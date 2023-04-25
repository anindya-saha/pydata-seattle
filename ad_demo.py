import datetime
from collections import defaultdict
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd
import plotly.express as px
import shap
import statsforecast.models as statsFModels
from lightgbm import LGBMRegressor
from statsforecast import StatsForecast
from whylogs import DatasetProfileView


# plotly graph to show anomalies
def plot_series_graph(series: pd.Series, anomalies: Dict[str, List[datetime.datetime]]):
    _dict = defaultdict(set)

    for k, d in anomalies.items():
        for x in d:
            _dict[x].add(k)

    fig = px.line(series)

    for ts, algos in _dict.items():
        fig.add_vrect(
            x0=ts - datetime.timedelta(days=1),
            x1=ts,
            line_width=0,
            fillcolor="red",
            opacity=0.1 * len(algos),
            annotation_text="<br>".join(algos),
            annotation_position="bottom right",
        )
    fig.update_layout(showlegend=True)
    return fig


def plot_feature_drift_stack(importance: pd.DataFrame):
    fig = px.bar(importance, y="name", x="importance", orientation="h")
    fig.update_layout(yaxis={"title": "", "dtick": 1})
    return fig


def get_feature_drift_stack(features_df: pd.DataFrame):
    x = features_df.reset_index(drop=True)
    y = features_df[["_pred"]].reset_index(drop=True)
    x = x.drop(columns=["_pred"])
    model = LGBMRegressor().fit(x.diff().loc[1:, :], y.diff().loc[1:])

    explainer = shap.Explainer(model)
    shap_values = explainer(x.diff().loc[1:, :])
    vals = np.abs(shap_values.values).mean(0)
    feature_names = x.columns

    feature_importance = pd.DataFrame(
        list(zip(feature_names, vals)), columns=["name", "importance"]
    )
    feature_importance = feature_importance.sort_values(
        by=["importance"], ascending=False
    ).sort_values("importance")
    feature_importance = feature_importance[feature_importance.importance > 0]

    importance = feature_importance.sort_values("importance")
    return importance


# extract feature and prediction data from the give profile
def extract_profiles(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    features = []
    preds = []

    for fv, pv in zip(
        df.features_profile.apply(DatasetProfileView.deserialize),
        df.predictions_profile.apply(DatasetProfileView.deserialize),
    ):
        # capture the mean of features
        series = fv.to_pandas()[["distribution/mean"]]
        features.append(series["distribution/mean"])

        series = pv.to_pandas()
        preds.append(series[series.index == "predictions"])

    idx = pd.to_datetime(df.date)

    # get all whylog metrics for predictions
    preds_df = pd.concat(preds).reset_index(drop=True).set_index(idx)

    # get distribution/mean whylog metric for features
    features_df = (
        pd.concat([x.to_frame().T for x in features])
        .reset_index(drop=True)
        .set_index(idx)
    )

    return preds_df, features_df


class MSTLDetector:
    _models: List[Any]
    _metric: str
    _level: List[float]

    @property
    def name(self) -> str:
        return "MSTL" + self._metric.split("/")[-1]

    def __init__(
        self,
        metric: str,
        season: Union[int, List],
        level: float,
    ):
        self._models = [
            statsFModels.MSTL(season_length=season, trend_forecaster=statsFModels.AutoARIMA())
        ]
        self._metric = metric
        self._level = [level]

    def score(
        self,
        preds_df: pd.DataFrame,
        freq: str = "D",  # data frequency in input data set
        horizon: int = 2,  # horizon for predictions
    ) -> pd.DataFrame:
        # statsforecast expects the dataframe with these columns
        df = pd.DataFrame(
            dict(unique_id="model_name", ds=preds_df.index, y=preds_df[self._metric])
        )
        statsf = StatsForecast(df=df, models=self._models, freq=freq)

        # generate forecasts for horizon. Enabling "fitted" allows to retrofit forecasts to existing data
        forecasts = statsf.forecast(
            h=horizon, fitted=True, level=self._level
        ).reset_index()
        fitted_df = statsf.forecast_fitted_values().reset_index()

        return (
            pd.concat([fitted_df, forecasts])
            .set_index("ds")
            .rename(columns={"ds": "date"})
        )

    def find_anomalies(self, df: pd.DataFrame) -> List[datetime.datetime]:
        if df.empty:
            return []

        return df[
            (df.y > df["MSTL-hi-99.9"]) | (df.y < df["MSTL-lo-99.9"])
        ].index.tolist()
