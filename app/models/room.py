from .database import Base, SessionLocal
from sqlalchemy import Integer, Column, Text, exc
from ..schemas.room import RoomSchema


class Room(Base):

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, nullable=False, unique=True)
    name = Column(Text, nullable=True)

    def __init__(self, id: int, room_id: int, name: str):
        self.id = id
        self.room_id = room_id
        self.name = name

    def __repr__(self):
        return f"<room_id = {self.room_id}>"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "name": self.name
        }


# FAT MODEL WITH SESSION

session = SessionLocal()


def create_room_dto(room: RoomSchema):
    new_room_dto = Room(room.id, room.room_id, room.name)
    try:
        session.add(new_room_dto)
        session.commit()
        return new_room_dto
    except exc.SQLAlchemyError as ex:
        session.rollback()
        raise ex


def delete_room_by_id(room: RoomSchema):
    try:
        session.query(Room).filter(Room.room_id == room.room_id).delete()
        session.commit()
    except exc.SQLAlchemyError as ex:
        session.rollback()
        raise ex
