from typing import Optional
from pydantic import BaseModel


class Accounting(BaseModel):
    accounting_id: int
    client_id: str
    location_id: str
    status: bool
    error: Optional[str] = None
    ort_session_time: Optional[float] = None
    matting_time: Optional[float] = None
    main_operation_time: Optional[float] = None
    image_download_time: Optional[float] = None
