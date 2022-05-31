from os import environ

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_DRIVER = "postgresql"
DB_USERNAME = "admin"
DB_PASSWORD = "admin"
DB_HOST_ADDRESS = "postgres"
DB_PORT = "5432"
DB_NAME = "miniumbrelladb"


# Production
uri = environ.get("DATABASE_URL") or None
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
else:
    uri = f"{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST_ADDRESS}:{DB_PORT}/{DB_NAME}"

engine = create_engine(uri, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
