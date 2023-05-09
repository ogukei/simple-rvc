from argh import ArghParser

from .converters import convert_hubert, convert_rvc, convert_vits
from .tools import eval_dataset, list_audio_devices, realtime_vc, export_onnx

parser = ArghParser()
parser.add_commands(
    [
        convert_hubert,
        convert_vits,
        convert_rvc,
        realtime_vc,
        eval_dataset,
        list_audio_devices,
        export_onnx,
    ]
)
parser.dispatch()
