
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

RUN apt-get update
RUN apt-get install -y python3-pip wget espeak gosu libsndfile1-dev git
#RUN apt-get clean
#RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

# install the dependencies using Poetry
COPY pyproject.toml poetry.lock .

RUN pip install poetry==1.4.2
RUN poetry install --no-root

# download weights
# https://github.com/w-okada/voice-changer/blob/04c009416ab1cf6d6c232eb0b2d62b691bad7ec3/README_dev_en.md
RUN wget https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/1c75048c96f23f99da4b12909b532b5983290d7d/hubert_base.pt
RUN wget https://github.com/bshall/hubert/releases/download/v0.1/hubert-soft-0d54a1f4.pt
RUN wget https://github.com/openvpi/vocoders/releases/download/nsf-hifigan-v1/nsf_hifigan_20221211.zip

RUN apt-get install -y unzip
RUN unzip nsf_hifigan_20221211.zip

# sudo docker build -t simple_rvc .
# sudo docker run --rm --runtime=nvidia --gpus all --name vc -it --entrypoint /bin/bash -v .:/workspace simple_rvc

# poetry run python ../workspace/src/main.py
