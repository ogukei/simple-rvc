
from VoiceChangerManager import VoiceChangerManager
import torch
import json
import numpy as np
from scipy.io.wavfile import read, write

def main():
    # adjustment
    # +10 ~ +20: female to male
    # -10 ~ -20: male to female
    trans = 12
    pth_model_filename = '../workspace/models/Tuki03.pth'
    input_audio_filename = '../workspace/input.wav'
    output_audio_filename = '../workspace/output.wav'
    # check cuda
    if torch.cuda.is_available():
        print("Attempting to use CUDA")
    else:
        print("CUDA not available")
    # init
    # @see https://github.com/w-okada/voice-changer/blob/a68bd1d8997b2fe493bcff3807373c485c32aed6/server/MMVCServerSIO.py#L85
    # @see https://github.com/w-okada/voice-changer/blob/04c009416ab1cf6d6c232eb0b2d62b691bad7ec3/start_docker.sh#L31
    # @see https://github.com/w-okada/voice-changer/blob/04c009416ab1cf6d6c232eb0b2d62b691bad7ec3/README_dev_en.md
    voice_changer_manager = VoiceChangerManager.get_instance({
        # content_vec is unnecessary for RVC
        "content_vec_500": '',
        "content_vec_500_onnx": '',
        "content_vec_500_onnx_on": '',
        "hubert_base": 'hubert_base.pt',
        "hubert_soft": 'hubert-soft-0d54a1f4.pt',
        "nsf_hifigan": 'nsf_hifigan/model',
    })
    # https://github.com/w-okada/voice-changer/blob/08d07c599718a1395ae6a4d1eda71de1f8defd88/server/restapi/MMVC_Rest_Fileuploader.py#L67
    # https://github.com/w-okada/voice-changer/blob/8a17da84cf0f8e267b1efa57a217e4f3e7895ac0/client/lib/src/hooks/useServerSetting.ts#L13
    # https://github.com/w-okada/voice-changer/blob/0250541fd0691a3c49bf956eeacf30266b734b84/server/voice_changer/RVC/RVC.py#L108
    props = {
        'slot': 0,
        'isHalf': True,
        'files': {
            'configFilename': None,
            'pyTorchModelFilename': pth_model_filename,
            'onnxModelFilename': None,
            'featureFilename': None,
            'indexFilename': None,
        },
        'params': json.dumps({
            'trans': trans,
            'f0Detector': 'harvest',
            'rvcQuality': 3,
        })
    }
    # selecting model type
    switch_result = voice_changer_manager.switchModelType('RVC')
    print("switchResult:")
    print(switch_result)
    # model loading
    load_model_result = voice_changer_manager.loadModel(props)
    print("loadModel result:")
    print(load_model_result)
    # processing
    # https://github.com/w-okada/voice-changer/commit/de1043aa8aa61d352e30977b84241ee453c35537
    sample_rate, input_audio = read(input_audio_filename)
    assert(sample_rate == 48000)
    # expects 48000Hz single channel 16bit signed audio
    output_audio = np.array([])
    chunk_size = 4096
    for i in range(0, len(input_audio), chunk_size):
        print(f'processing samples {i}/{len(input_audio)}...')
        chunk = input_audio[i:i+chunk_size]
        chunk = chunk.ravel()
        # zero fill
        if len(chunk) < chunk_size:
            zero_padding = np.zeros((chunk_size - len(chunk),))
            chunk = np.concatenate([chunk, zero_padding])
        assert(len(chunk) == chunk_size)
        processed_chunk, _ = voice_changer_manager.changeVoice(chunk)
        output_audio = np.concatenate([output_audio, processed_chunk])
    write(output_audio_filename, 48000, np.int16(output_audio))
    print('DONE!')

if __name__ == '__main__':
    main()
