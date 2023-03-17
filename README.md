# Anomaly Detection at Scale with Whylogs


This command pulls the jupyter/scipy-notebook latest image from Docker Hub if it is not already present on the local host. 
It then starts an ephemeral container running a Jupyter Server and exposes the server on host port 10000.
```
docker run -it --rm -p 10000:8888 -e JUPYTER_TOKEN='' -v "${PWD}":/home/jovyan/work jupyter/scipy-notebook:latest

pip install -r requirements.txt
```

The use of the `-v` flag in the command mounts the current working directory on the host (${PWD} in the example command) 
as /home/jovyan/work in the container. The server logs appear in the terminal.

Visiting `http://<hostname>:10000/?token=<token>` in a browser loads JupyterLab.

Due to the usage of the flag `--rm` Docker automatically cleans up the container and removes the file system 
when the container exits, but any changes made to the `~/work` directory and its files in the container will 
remain intact on the host. The `-it` flag allocates pseudo-TTY.

You can also build and run the Docker container locally.

```
docker build -t pydata-seattle:1.0 -f Dockerfile .
docker run -it --rm -p 8888:8888 -v "${PWD}":/home/jovyan/work pydata-seattle:1.0
```

