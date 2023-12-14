from db import crud
from utils.hash import hash
from typing import Annotated
from settings import settings
from dependencies.db import get_db
from sqlalchemy.orm import Session
from fastapi.security import APIKeyHeader
from fastapi import status, Depends, HTTPException


api_key_header = APIKeyHeader(name="x-api-key")


def get_client(
    key: Annotated[str, Depends(api_key_header)], db: Session = Depends(get_db)
):
    hashed_key = hash(key)
    client = crud.client.get_by_api_key(db, hashed_key)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return client


def authenticate_admin(key: Annotated[str, Depends(api_key_header)]):
    if hash(key) != settings.admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing admin API Key",
        )
