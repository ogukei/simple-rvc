
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

# for realtime processing
RUN apt-get install -y alsa-base alsa-utils

# for onnx export 
RUN pip3 install onnx onnxruntime

# Debug: overwrite sources
RUN rm -rf hf_rvc
RUN ln -s ../../workspace/hf-rvc/hf_rvc ./hf_rvc
RUN pip3 install .

# sudo docker build -t simple_rvc .
# sudo docker compose up -d
# sudo docker compose exec simple_rvc /bin/bash
# python3 -m hf_rvc convert-rvc --hubert-path hubert_base.pt --unsafe ../../workspace/models/AISO-SYAKITTO.pth
# python3 -m hf_rvc export-onnx --hubert-path hubert_base.pt --output-path ../../workspace/models/a.onnx --unsafe ../../workspace/models/AISO-SYAKITTO.pth
