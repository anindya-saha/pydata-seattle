FROM jupyter/scipy-notebook:latest

USER root

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip -d /tmp && \
    /tmp/aws/install && \
    rm awscliv2.zip

COPY requirements.txt /home/jovyan/work/requirements.txt

RUN pip install -r /home/jovyan/work/requirements.txt

RUN chmod -R 777 /opt/conda/lib/python3.10/site-packages/whylogs/viz/html/

USER ${NB_UID}

WORKDIR "${HOME}"

# RUN git clone https://github.com/anindya-saha/pydata-seattle.git

COPY addemo23 addemo23/
COPY images/ images/
COPY Anomaly-detection.ipynb .
COPY Distributed-profiling.ipynb .
COPY ad_demo.py .
COPY README.md .

#USER root

#USER ${NB_UID}

CMD ["start-notebook.sh"]