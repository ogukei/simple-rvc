
from os import PathLike
from pathlib import Path

from transformers import HubertConfig, HubertForCTC

import torch
import torch.onnx

from ..converters.convert_hubert import (
    extract_hubert_config,
    extract_hubert_state,
    load_fairseq_hubert,
)
from ..converters.convert_vits import (
    extract_vits_config,
    extract_vits_state,
    load_vits_checkpoint,
)
from ..models.configuration_rvc import RVCConfig
from ..models.feature_extraction_rvc import RVCFeatureExtractor
from ..models.modeling_rvc import RVCModel
from ..models.vits.models import (
    SynthesizerTrnMs256NSFsid,
    SynthesizerTrnMs256NSFsidConfig,
)

def export_onnx(
    vits_path: str | PathLike,
    output_path: str | PathLike = "./models/out.onnx",
    save_directory: str | PathLike | None = None,
    hubert_path: str | PathLike = "./models/hubert_base",
    f0_method: str = "pm",
    unsafe: bool = False,
    safe_serialization=True,
):
    """Export onnx.

    Args:
        vits_path: Path to the original VITS checkpoint.
        save_directory: Directory to save the converted RVC model (optional).
        hubert_path: Path to the original Hubert model (default: "./models/hubert_base").
        f0_method: F0 extraction method, "pm" or "harvest" (default: "pm").
        unsafe: Set to True to load untrusted models (default: False).
        safe_serialization: Set to False to disable safe serialization (default: True).
    """

    if save_directory is None:
        p = Path(vits_path)
        save_directory = p.parent / p.stem

    if Path(hubert_path).is_file():
        fairseq_hubert = load_fairseq_hubert(str(hubert_path), unsafe)
        hubert_config = extract_hubert_config(fairseq_hubert)
        hubert_state = extract_hubert_state(hubert_config, fairseq_hubert)
    else:
        hubert_config = HubertConfig.from_pretrained(hubert_path)
        hubert_model = HubertForCTC.from_pretrained(hubert_path)
        assert isinstance(hubert_model, HubertForCTC)
        hubert_state = hubert_model.state_dict()

    assert isinstance(hubert_config, HubertConfig)

    if Path(vits_path).is_file():
        vits_checkpoint = load_vits_checkpoint(vits_path)
        vits_config = extract_vits_config(vits_checkpoint)
        vits_state = extract_vits_state(vits_checkpoint)
        vits_strict = False
    else:
        vits_config = SynthesizerTrnMs256NSFsidConfig.from_pretrained(vits_path)
        assert isinstance(vits_config, SynthesizerTrnMs256NSFsidConfig)
        vits = SynthesizerTrnMs256NSFsid.from_pretrained(vits_path)
        assert isinstance(vits, SynthesizerTrnMs256NSFsid)
        vits_state = vits.state_dict()
        vits_strict = True

    model = RVCModel(
        RVCConfig(
            hubert=hubert_config,
            vits=vits_config,
        )
    )

    # load state
    model.hubert.load_state_dict(hubert_state)
    model.vits.load_state_dict(vits_state, strict=vits_strict)

    model.eval()
    model.to("cpu")

    dummy_input_values = torch.randn(1, 16000, dtype=torch.float32)
    dummy_f0_coarse = torch.zeros(1, 100, dtype=torch.int32)
    dummy_f0 = torch.randn(1, 100, dtype=torch.float32)

    # export
    torch.onnx.export(
        model,
        (dummy_input_values, dummy_f0_coarse, dummy_f0),
        output_path,
        opset_version=15,
        input_names=["input_values", "f0_coarse", "f0"],
        output_names=["output"],
        dynamic_axes={
            "input_values": {0: "batch", 1: "sequence"},
            "f0_coarse": {0: "batch", 1: "sequence"},
            "f0": {0: "batch", 1: "sequence"},
            "output": {0: "batch", 1: "sequence"},
        },
    )

    return model


if __name__ == "__main__":
    from argh import ArghParser

    parser = ArghParser()
    parser.set_default_command(export_onnx)
    parser.dispatch()
