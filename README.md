
## Simple RVC

Heavily WIP.

Provides an easy-to-use command-line tool to apply voice conversion with RVC.

## Setup

### Build Docker Image
Requires NVIDIA GPUs capable of running CUDA at the moment. Ubuntu 22.04 LTS is recommended to host containers.

1. Install NVIDIA Container Toolkit
    * https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#installing-on-ubuntu-and-debian
1. Create image by running the following command
```
cd simple-rvs
sudo docker build -t simple_rvs .
```

### Prepare Files

1. Download the .pth model such as [天之つき学習モデル](https://amanotuki.booth.pm/items/4693675) and place it in `models/`
1. Make sure the filename matches as `pth_model_filename` specified in `src/main.py`
1. Create `input.wav` for your audio conversion input. Here is an example command using FFmpeg for preparing an input audio file.
```
cd simple-rvs
ffmpeg -i raw_audio.mp3 -ss 00:00:00 -t 00:00:30 -c:a pcm_s16le -ar 48000 -ac 1 input.wav
```

### Run
1. Run the following command

```
sudo docker run -it \
  -v .:/workspace \
  --rm \
  --runtime=nvidia \
  --gpus all \
  --entrypoint /bin/bash \
  simple_rvs

# make sure input.wav exists at `../workspace`
poetry run python ../workspace/src/main.py

# output.wav will be generated in `../workspace`
exit
```

## Links

https://amanotuki.booth.pm/items/4693675

https://github.com/w-okada/voice-changer

https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI

https://note.com/omiz_aiart/n/n558e45e36e13
