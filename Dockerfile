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

COPY . .

# CMD ["start-notebook.sh", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''", "--NotebookApp.allow_origin='*'"]

CMD ["start-notebook.sh", "--NotebookApp.open_browser=False"]