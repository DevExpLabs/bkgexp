from PIL import Image
from io import BytesIO
from fastapi import HTTPException
from tempfile import TemporaryFile
from settings import settings


def getImageFromFile(imageFile: TemporaryFile) -> Image:
    try:
        return Image.open(imageFile)
    except Exception as e:
        print(f"Failed to open image, {e}")
        raise HTTPException(status_code=422, detail=f"Failed to open image, {e}")


def getBytesFromImageFile(imageFile: TemporaryFile):
    image = getImageFromFile(imageFile)
    bts = BytesIO()
    image.save(bts, format=settings.image_format)
    bts.seek(0)
    return bts
