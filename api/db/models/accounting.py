from db.database import Base
from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey


class Accounting(Base):
    __tablename__ = "accounting"

    accounting_id = Column(Integer, primary_key=True)
    client_id = Column(String(36), ForeignKey("client.client_id"))
    location_id = Column(String(36), ForeignKey("client.location_id"))
    status = Column(Boolean)
    error = Column(String, nullable=True)
    ort_session_time = Column(Float, nullable=True)
    matting_time = Column(Float, nullable=True)
    main_operation_time = Column(Float, nullable=True)
    image_download_time = Column(Float, nullable=True)

    def __repr__(self) -> str:
        return (
            f"<{self.__name__}("
            f"accounting_id='{self.accounting_id}',"
            f"client_id='{self.client_id}',"
            f"location_id='{self.location_id}',"
            f"status='{self.status}',"
            f"error='{self.error}',"
            f"ort_session_time='{self.ort_session_time}',"
            f"matting_time='{self.matting_time}',"
            f"main_operation_time='{self.main_operation_time}',"
            f"image_download_time='{self.image_download_time}'"
            ")>"
        )
