from pydantic import BaseModel


class RunpodResponseTimings(BaseModel):
    ort_session_time: float
    matting_time: float
    main_operation_time: float
    image_download_time: float


class RunpodResponseError(BaseModel):
    error: str


class RunpodOutput(BaseModel):
    imageUrl: str
    timings: RunpodResponseTimings


class RunpodResponse(BaseModel):
    output: RunpodOutput
