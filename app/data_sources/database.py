from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_DRIVER = "postgresql"
DB_USERNAME = "admin"
DB_PASSWORD = "admin"
DB_HOST_ADDRESS = "postgres"
DB_PORT = "5432"
DB_NAME = "miniumbrelladb"

engine = create_engine(f"{DB_DRIVER}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST_ADDRESS}:{DB_PORT}/{DB_NAME}", echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
