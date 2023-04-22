# Anomaly Detection at Scale with Whylogs

Welcome to the Anomaly Detection Demo!

**Prerequisites:** Docker Desktop or Docker daemon running on your machine.

## Using the pre-built docker container
We have provided a docker image that you can run on your local machine and follow along the notebooks with the instructor.

The AWS credentials to download the data files from AWS S3 will be provided during the live workshop.

```
export DOCKER_DEFAULT_PLATFORM=linux/amd64
export AWS_ACCESS_KEY_ID=<provided during demo>
export AWS_SECRET_ACCESS_KEY=<provided during demo>

docker run -it --env GRANT_SUDO=yes --user root --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --rm -p 8888:8888 -v "${PWD}":/home/jovyan/work anindyas/pydata-seattle:1.0
```
If you also run Ray, the use
```
docker run -it --shm-size=10gb --env GRANT_SUDO=yes --user root --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --rm -p 8888:8888 -p 8265:8265 -v "${PWD}":/home/jovyan/work anindyas/pydata-seattle:1.0
```

The use of the `-v` flag in the command mounts the current working directory on the host (${PWD} in the command) 
as /home/jovyan/work in the container. The server logs appear in the terminal.

Using `--user root` will spawn the jupyter notebook with jovyan having root privileges.

Due to the usage of the flag `--rm` Docker automatically cleans up the container and removes the file system 
when the container exits, but any changes made to the `~/work` directory and its files in the container will 
remain intact on the host. The `-it` flag allocates pseudo-TTY.

## Building your own docker container
You can also build and run the Docker container locally.

```
export DOCKER_DEFAULT_PLATFORM=linux/amd64
export AWS_ACCESS_KEY_ID=<provided during demo>
export AWS_SECRET_ACCESS_KEY=<provided during demo>

docker build -t pydata-seattle:1.0 -f Dockerfile .
docker run -it --env GRANT_SUDO=yes --env AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} --env AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} --rm -p 8888:8888 -v "${PWD}":/home/jovyan/work anindyas/pydata-seattle:1.0
```

## Download file from S3 bucket
Once the docker container is up, connect to the Jupyterlab.
Open a terminal from the launcher tab and download the relevant data from the S3 bucket

```bash
aws s3 cp s3://addemo23/ work/addemo23/ --recursive
```

