from pydantic import BaseModel


class RoomSchema(BaseModel):
    id: int
    room_id: int
    name: str
