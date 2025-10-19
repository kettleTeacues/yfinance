FROM python:3.13-slim

ENV USERNAME=yf
ENV PYTHONPATH=/home/$USERNAME

RUN apt-get update && \
    apt-get install -y \
    nano curl wget git \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r $USERNAME && useradd -r -g $USERNAME $USERNAME
WORKDIR /home/$USERNAME

COPY ./utils ./utils
COPY ./commands ./commands
COPY ./database ./database
COPY ./insert_yf ./insert_yf
COPY ./models ./models
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

USER $USERNAME
