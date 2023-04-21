FROM jupyter/scipy-notebook:latest

USER root

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm awscliv2.zip


COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt && \
    rm requirements.txt

RUN chmod -R 777 /opt/conda/lib/python3.10/site-packages/whylogs/viz/html/

USER ${NB_UID}

WORKDIR "${HOME}"

CMD ["start-notebook.sh"]