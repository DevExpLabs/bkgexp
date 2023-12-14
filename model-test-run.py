from ml import model
from PIL import Image

source_image = Image.open('input-bike.png').convert('RGB')

mask, cutout = model.run(source_image)

(Image.fromarray(mask)).show('mask')
(Image.fromarray(cutout)).show('other')
