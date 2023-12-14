import torch, cv2
import numpy as np
from PIL import Image

from time import time

def FB_blur_fusion_foreground_estimator_2(image, alpha, r=90):
    alpha = alpha[:, :, None]
    F, blur_B = FB_blur_fusion_foreground_estimator(
        image, image, image, alpha, r)
    return FB_blur_fusion_foreground_estimator(image, F, blur_B, alpha, r=6)[0]

def FB_blur_fusion_foreground_estimator(image, F, B, alpha, r=90):
    blurred_alpha = cv2.blur(alpha, (r, r))[:, :, None]

    blurred_FA = cv2.blur(F * alpha, (r, r))
    blurred_F = blurred_FA / (blurred_alpha + 1e-5)

    blurred_B1A = cv2.blur(B * (1 - alpha), (r, r))
    blurred_B = blurred_B1A / ((1 - blurred_alpha) + 1e-5)
    F = blurred_F + alpha * \
        (image - alpha * blurred_F - (1 - alpha) * blurred_B)
    F = np.clip(F, 0, 1)
    return F, blurred_B

def generate_output(image, mask):
    image = np.asarray(image)
    mask = mask.convert('L')
    mask = np.asarray(mask)

    matting_time = time()
    foreground = FB_blur_fusion_foreground_estimator_2(image / 255, mask / 255.0)
    matting_time = time() - matting_time
    print(f'Alpha matting run time: {matting_time}[s]')

    foreground = foreground * 255
    return np.concatenate([foreground, mask[:, :, np.newaxis]], axis=2).astype(np.uint8), matting_time

class static_resize:
    def __init__(self, size=[1024, 1024]): 
        self.size = size
                    
    def __call__(self, img):
        return img.resize(self.size, Image.BILINEAR)    

class normalize:
  def __init__(self, mean=None, std=None, div=255):
    self.mean = mean if mean is not None else 0.0
    self.std = std if std is not None else 1.0
    self.div = div
      
  def __call__(self, img):
    img /= self.div
    img -= self.mean
    img /= self.std
        
    return img
  
class tonumpy:
  def __init__(self):
    pass

  def __call__(self, img):
    img = np.array(img, dtype=np.float32)
    return img
  
class totensor:
  def __init__(self):
    pass

  def __call__(self, img):
    img = img.transpose((2, 0, 1))
    img = torch.from_numpy(img).float()
    
    return img
