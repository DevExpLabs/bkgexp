from schemas.client import Client
from dependencies.db import get_db
from sqlalchemy.orm import Session
from db.crud import client as client_crud
from routers.authentication import authenticate_admin
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(
    prefix="/admin", tags=["admin"], dependencies=[Depends(authenticate_admin)]
)


@router.post("/client")
def create_client(db: Session = Depends(get_db)) -> Client:
    api_key_raw, client = client_crud.create(db)
    return Client(
        client_id=client.client_id, location_id=client.location_id, api_key=api_key_raw
    )


@router.post("/location/{client_id}")
def create_location(client_id: str, db: Session = Depends(get_db)) -> Client:
    try:
        api_key_raw, client = client_crud.create_location(db, client_id)
    except Exception as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return Client(
        client_id=client.client_id, location_id=client.location_id, api_key=api_key_raw
    )


@router.delete("/location/{location_id}")
def remove_location(location_id: str, db: Session = Depends(get_db)) -> bool:
    try:
        res = client_crud.remove(db, location_id=location_id)
    except Exception as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
    return res


@router.delete("/client/{client_id}")
def remove_client(client_id: str, db: Session = Depends(get_db)) -> bool:
    try:
        res = client_crud.remove(db, client_id=client_id)
    except Exception as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return res
