from pydantic import BaseModel


class ClientBase(BaseModel):
    client_id: str
    location_id: str


class Client(ClientBase):
    api_key: str
