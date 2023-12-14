from utils.hash import hash
from typing import Annotated
from schemas.client import ClientBase
from sqlalchemy.orm import Session
from dependencies.db import get_db
from db.crud import client as client_crud
from schemas.auth import AuthBody, BadCredentials
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "", responses={401: {"description": "Bad credentials", "model": BadCredentials}}
)
def auth(body: AuthBody, db: Annotated[Session, Depends(get_db)]) -> ClientBase:
    client = client_crud.get_by_api_key(db, hash(body.api_key))
    if not client:
        raise HTTPException(status_code=401, detail="Bad credentials")

    return client
