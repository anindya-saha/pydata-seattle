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
export DOCKER_DEFAULT_PLATFORM=linux/amd64
export AWS_ACCESS_KEY_ID=<provided during demo>
export AWS_SECRET_ACCESS_KEY=<provided during demo>

docker build -t pydata-seattle:1.0 -f Dockerfile .
docker run -it --env GRANT_SUDO=yes --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --rm -p 8888:8888 -v "${PWD}":/home/jovyan/work pydata-seattle:1.0
```
Copy over the data file to S3 bukcket
aws s3 cp addemo23/ s3://addemo23/ --recursive

Download file from S3 bucket
aws s3 cp s3://addemo23/ addemo23/ --recursive --dryrun

