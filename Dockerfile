
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

RUN apt-get update
RUN apt-get install -y python3-pip wget espeak gosu libsndfile1-dev git
#RUN apt-get clean
#RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

# pyaudio
RUN apt-get install -y portaudio19-dev

# build hf-rvc
RUN git clone https://github.com/esnya/hf-rvc.git
WORKDIR hf-rvc
RUN git reset --hard 8629255960fca2fbf1c1eeec0290e5624913e2a9

RUN pip3 install .

# install some missing dependencies for HF RVC Command Line Tools
RUN pip3 install pyaudio==0.2.13
RUN pip3 install praat-parselmouth==0.4.3
RUN pip3 install fairseq==0.12.2

RUN wget https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/1c75048c96f23f99da4b12909b532b5983290d7d/hubert_base.pt

RUN apt-get install -y alsa-base alsa-utils

# Debug: overwrite sources
RUN rm -rf hf_rvc
RUN ln -s ../../workspace/hf-rvc/hf_rvc ./hf_rvc
RUN pip3 install .

# # download weights
# # https://github.com/w-okada/voice-changer/blob/04c009416ab1cf6d6c232eb0b2d62b691bad7ec3/README_dev_en.md
# RUN wget https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/1c75048c96f23f99da4b12909b532b5983290d7d/hubert_base.pt
# RUN wget https://github.com/bshall/hubert/releases/download/v0.1/hubert-soft-0d54a1f4.pt
# RUN wget https://github.com/openvpi/vocoders/releases/download/nsf-hifigan-v1/nsf_hifigan_20221211.zip

# RUN apt-get install -y unzip
# RUN unzip nsf_hifigan_20221211.zip

# sudo docker build -t simple_rvc .
# sudo docker run --rm --runtime=nvidia --gpus all --name vc -it --entrypoint /bin/bash -v .:/workspace simple_rvc

# sudo docker build -t simple_rvc .
# sudo docker compose up -d
# sudo docker compose exec simple_rvc /bin/bash
# python3 -m hf_rvc convert-rvc --hubert-path hubert_base.pt --unsafe ../../workspace/models/AISO-SYAKITTO.pth
# python3 -m hf_rvc 
# https://pbaumgarten.com/python/audio.md
# https://leimao.github.io/blog/Docker-Container-Audio/
