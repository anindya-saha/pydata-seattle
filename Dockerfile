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

USER ${NB_UID}

WORKDIR "${HOME}"

RUN git clone https://github.com/anindya-saha/pydata-seattle.git
COPY addemo23 pydata-seattle/addemo23/

USER root

RUN pip install -r pydata-seattle/requirements.txt

RUN chmod -R 777 /opt/conda/lib/python3.10/site-packages/whylogs/viz/html/

USER ${NB_UID}

CMD ["start-notebook.sh"]