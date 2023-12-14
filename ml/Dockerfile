FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu22.04

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND=noninteractive
ENV SHELL=/bin/bash
ENV PYTHONUNBUFFERED=1
# prevents python creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update -y && \
    apt install -y \
    software-properties-common \
    curl \
    wget

RUN add-apt-repository ppa:deadsnakes/ppa -y

RUN apt install -y \
    python3.10 \
    python3.10-distutils \
    ffmpeg \
    libsm6 \
    libxext6

RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

COPY ./ml .

RUN wget https://ml-model.aishoot.co/bkg-rm/latest.onnx -O ./model/latest.onnx

RUN pip3.10 install -r runpod_requirements.txt

CMD [ "python3.10", "runner.py" ]
