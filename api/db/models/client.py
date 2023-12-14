from db.database import Base
from sqlalchemy import Column, String


class Client(Base):
    __tablename__ = "client"

    client_id = Column(String(36), primary_key=True)
    location_id = Column(String(36), primary_key=True)
    api_key = Column(String(64))

    def __repr__(self) -> str:
        return (
            f"<Client("
            f"client_id='{self.client_id}',"
            f"location_id='{self.location_id}',"
            f"api_key='{self.api_key}'"
            ")>"
        )
