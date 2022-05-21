from pydantic import BaseModel


class RoomSchema(BaseModel):
    room_id: int
