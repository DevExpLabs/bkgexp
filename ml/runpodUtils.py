import requests
from PIL import Image
from time import time
from io import BytesIO
from requests import Response


def downloadImage(fileUrl: str) -> (Response, float):
    try:
        image_download_time = time()

        response = requests.get(fileUrl)
        response.raise_for_status()

        image_download_time = time() - image_download_time
        print(f"Image download time: {image_download_time}[s]")

        return response, image_download_time
    except requests.exceptions.RequestException as e:
        print(f"Failed to get an image from remote: {e}")
        raise Exception(f"Failed to get an image from remote: {e}")


def getImageFromResponse(response: Response) -> Image:
    try:
        image = Image.open(BytesIO(response.content))
        return image
    except Exception as e:
        print(f"Failed to load an image: {e}")
        raise Exception(f"Failed to load an image: {e}")
