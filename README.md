
## Simple RVC

(WIP) Provides an easy-to-use command-line tool to apply voice conversion with RVC.

Heavily WIP. Currently just wraps the [hf-rvc](https://github.com/esnya/hf-rvc) and added some tweaks to the code to export ONNX models.

## Setup

### Build Docker Image
Requires NVIDIA GPUs capable of running CUDA at the moment. Ubuntu 22.04 LTS is recommended to host containers.

1. Install NVIDIA Container Toolkit
    * https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#installing-on-ubuntu-and-debian
1. Create image by running the following command
```
cd simple-rvc
sudo docker build -t simple_rvc .
```

### Run
1. Run the following command to export ONNX models.
    * Make sure `./models/model.pth` exists

```
sudo docker compose up -d
sudo docker compose exec simple_rvc /bin/bash
python3 -m hf_rvc export-onnx --hubert-path hubert_base.pt \
--output-path ../../workspace/models/a.onnx \
--unsafe ../../workspace/models/model.pth
```

## Links

https://github.com/esnya/hf-rvc

https://github.com/w-okada/voice-changer

https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI
