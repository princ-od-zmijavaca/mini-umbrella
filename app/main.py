from fastapi import FastAPI

from app.models.database import engine, Base
from app.routers.room_router import room_router
from app.routers.user_router import user_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(room_router)

app.include_router(user_router)
