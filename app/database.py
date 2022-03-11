from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALQUEMY_DATABASE_URL = "postgresql://<user>:<password>@<ip-address/hostname>/<database-name>"
SQLALQUEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/fast_api"

engine = create_engine(SQLALQUEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()