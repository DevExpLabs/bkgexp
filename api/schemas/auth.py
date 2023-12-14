from pydantic import BaseModel


class AuthBody(BaseModel):
    api_key: str


class BadCredentials(BaseModel):
    detail: str
