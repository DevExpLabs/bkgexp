import hashlib
from uuid import uuid4
from sqlalchemy import text
from settings import settings
from db.models.models import *
from db.database import Base, engine, SessionLocal


def create_tables():
    Base.metadata.create_all(bind=engine)


def insert_test_data():
    for i in range(5):
        client_id = uuid4()
        location_id = uuid4()
        api_key = uuid4()
        print(
            f"API key for (client_id={client_id}, location_id={location_id}):\n{api_key}"
        )
        api_key_hashed = hashlib.sha256(str(api_key).encode("utf8")).hexdigest()
        with SessionLocal() as session, session.begin():
            session.execute(
                text(
                    f"insert into client values ('{client_id}', '{location_id}', '{api_key_hashed}')"
                )
            )


def main() -> None:
    create_tables()
    if settings.env == "DEV":
        insert_test_data()


if __name__ == "__main__":
    main()
