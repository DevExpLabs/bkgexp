from dependencies.db import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from schemas.accounting import Accounting
from db.crud.accounting import accounting as accounting_crud

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/client/{client_id}")
def client_stats(client_id: str, db: Session = Depends(get_db)) -> list[Accounting]:
    return accounting_crud.read(db, client_id=client_id)


@router.get("/location/{location_id}")
def location_stats(location_id: str, db: Session = Depends(get_db)) -> list[Accounting]:
    return accounting_crud.read(db, location_id=location_id)
