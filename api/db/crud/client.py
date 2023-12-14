from uuid import uuid4
from utils.hash import hash
from sqlalchemy.orm import Session
from db.models.client import Client as ClientModel
from typing import Optional, TypeVar, Generic, Type


ModelType = TypeVar("ModelType", bound=ClientModel)


class Client(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_by_api_key(self, db: Session, key: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.api_key == key).first()

    def create(self, db: Session) -> tuple[str, ModelType]:
        api_key, api_key_hashed = self._generate_api_key()
        client = self.model(
            client_id=str(uuid4()), location_id=str(uuid4()), api_key=api_key_hashed
        )
        db.add(client)
        db.commit()
        return api_key, client

    def create_location(self, db: Session, client_id: str) -> tuple[str, ModelType]:
        client_exists = (
            db.query(self.model).filter(self.model.client_id == client_id).first()
            is not None
        )
        if not client_exists:
            raise Exception("Failed to find client")

        api_key, api_key_hashed = self._generate_api_key()
        client = self.model(
            client_id=client_id, location_id=str(uuid4()), api_key=api_key_hashed
        )
        db.add(client)
        db.commit()

        return api_key, client

    def remove(self, db: Session, **columns) -> bool:
        remove_count = db.query(self.model).filter_by(**columns).delete()
        if not remove_count:
            raise Exception("Failed to find item")

        db.commit()
        return True

    def _generate_api_key(self) -> tuple[str, str]:
        key = str(uuid4())
        key_hashed = hash(key)
        return key, key_hashed


client = Client(ClientModel)
