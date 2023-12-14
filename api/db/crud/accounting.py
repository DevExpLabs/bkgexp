from sqlalchemy.orm import Session
from typing import TypeVar, Generic, Type
from schemas.accounting import Accounting
from db.models.client import Client as ClientModel
from db.models.accounting import Accounting as AccountingModel


ModelType = TypeVar("ModelType", bound=AccountingModel)


class Accounting(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def read(self, db: Session, **column) -> list[Accounting]:
        return db.query(self.model).filter_by(**column).all()

    def create(
        self,
        db: Session,
        client: ClientModel,
        status: bool,
        error: str = None,
        ort_session_time: float = None,
        matting_time: float = None,
        main_operation_time: float = None,
        image_download_time: float = None,
    ):
        obj = self.model(
            client_id=client.client_id,
            location_id=client.location_id,
            status=status,
            error=error,
            ort_session_time=ort_session_time,
            matting_time=matting_time,
            main_operation_time=main_operation_time,
            image_download_time=image_download_time,
        )
        db.add(obj)
        db.commit()


accounting = Accounting(AccountingModel)
