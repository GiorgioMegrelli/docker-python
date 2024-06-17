# Docker for Python

A Dockerfile that attempts to install the Python 3.x distribution from all available versions listed on https://www.python.org/ftp/python/.
It downloads the source code from the website and installs it locally using the `make` command.

To see all available versions, run:
```shell
python python_versions.py
```

## Development

To set the desired Python version, specify it in the Dockerfile (the default version is `3.12.0`):
```dockerfile
ARG PYTHON_VERSION='<python-version>'
```

_or it can be passed while building the image_

Build docker image:
```shell
docker build -t py-dev .
```

Run container in interactive mode:
```shell
docker run -it --rm -v ${PWD}:/usr/src/app py-dev
```

_Written in Powershell_
