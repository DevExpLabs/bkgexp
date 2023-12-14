import uvicorn, os
from PIL import Image
from typing import Optional
from random import uniform
from handler import Handler
from fastapi import FastAPI
from model.model import Model
from pydantic import BaseModel


class EventInput(BaseModel):
    fileUrl: str


class Event(BaseModel):
    id: Optional[int] = 1
    input: EventInput


class HandlerMock(Handler):
    def get_source_image(self, file_url: str):
        # ⬇️ Uncomment to simulate runpod failure ⬇️
        # raise Exception("Manual exception raised")
        return Image.open(file_url), uniform(0, 1)


app = FastAPI()
model = Model()
handler = HandlerMock(model)


@app.post("/runsync")
def runsync(event: Event):
    handler_event = {"id": 1, "input": {"fileUrl": event.input.fileUrl}}

    # ⬇️ Runpod successful response shape ⬇️
    # {
    #     "output": {
    #         "imageUrl": "simulated_uploaded/6edc61d4.png",
    #         "timings": {
    #             "ort_session_time": 4.748099088668823,
    #             "matting_time": 0.0810098648071289,
    #             "main_operation_time": 4.956840991973877,
    #             "image_download_time": 0.7211310863494873,
    #         },
    #     }
    # }

    # 🚨 Runpod error response shape 🚨
    # {
    #     "error": "Error message"
    # }

    result = handler(handler_event)
    if "error" not in result:
        result["imageUrl"] = f"{os.getcwd()}/{result['imageUrl']}"
        result = {"output": result}
    return result


if __name__ == "__main__":
    uvicorn.run("local_server:app", host="0.0.0.0", port=8001, reload=True)
