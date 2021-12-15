from fastapi import APIRouter

from app.models.room import create_room_dto, delete_room_by_id
from app.schemas.room import RoomSchema

room_router = APIRouter()


@room_router.post("/createroom")
async def create_room(room: RoomSchema):
    response = create_room_dto(room)
    return response


@room_router.delete("/deleteroom")
def delete_room(room: RoomSchema):
    response = delete_room_by_id(room)
    return {"data": response}
