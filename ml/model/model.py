import torch, os
import numpy as np
import model.utils as utils
from PIL import Image
import onnxruntime as ort
import torch.nn.functional as F
import torchvision.transforms as transforms

from time import time

class Model:
  def __init__(self):
    so = ort.SessionOptions()
    so.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    self.ort_session = ort.InferenceSession(f'{os.path.dirname(__file__)}/latest.onnx', so, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])

  def _transform(self, image):
    return transforms.Compose([
      utils.static_resize(),
      utils.tonumpy(),
      utils.normalize(
        mean=[0.485, 0.456, 0.406], 
        std=[0.229, 0.224, 0.225]),
      utils.totensor()
      ]
    )(image)
  
  def run(self, inputImage: Image) -> tuple[np.array, np.array]:
    shape = inputImage.size[::-1]   
    image = self._transform(inputImage)
    image = image.unsqueeze(0)

    ort_session_time = time()
    pred = self.ort_session.run(None, {'input':  image.numpy()})
    ort_session_time = time() - ort_session_time
    print(f'ORT Session run time: {ort_session_time}[s]')

    pred = torch.from_numpy(pred[0]).float()
    pred = F.interpolate(pred, shape, mode='bilinear', align_corners=True)
    pred = pred.data.cpu()
    pred = pred.numpy().squeeze()

    mask = (np.stack([pred] * 3, axis=-1) * 255).astype(np.uint8)
    result, matting_time = utils.generate_output(
            inputImage,
            Image.fromarray(mask)
          )
    timings = {
      'ort_session_time': ort_session_time,
      'matting_time': matting_time
    }
    return mask, result, timings
