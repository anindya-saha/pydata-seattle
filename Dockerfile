FROM jupyter/scipy-notebook:latest

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ["start-notebook.sh"]