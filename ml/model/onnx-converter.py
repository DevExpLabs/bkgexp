# SHOULD BE FUN FROM: https://github.com/plemeri/InSPyReNet/tree/main
import onnx, torch
from onnxsim import simplify
from utils.misc import Simplify
from lib.InSPyReNet import InSPyReNet_SwinB
from onnxruntime.quantization import quantize_dynamic, QuantType


model = InSPyReNet_SwinB(64, True, [1024, 1024], threshold=None)
model.load_state_dict(torch.load("./snapshots/Plus_Ultra/latest.pth",  map_location=torch.device('cpu')))
model = Simplify(model)

data = torch.rand(1, 3, 1024, 1024)

output_file = "latest.onnx"
torch.onnx.export(model,
                  data,
                  output_file,
                  opset_version=20,
                  export_params=True,
                  input_names=['input'],
                  output_names = ['output'],
                  verbose=True)

onnx_model = onnx.load(output_file)
onnx_model, check = simplify(onnx_model)
assert check, "Simplified ONNX model could not be validated"
onnx.save(onnx_model, output_file)
