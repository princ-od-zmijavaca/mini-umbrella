import random

from app.data_sources.database import Base, SessionLocal
from sqlalchemy import Integer, Column, Text, exc, ARRAY
from ..schemas.room import RoomSchema
from ..schemas.vote import VoteSchema


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, nullable=False, unique=True)
    guest_count = Column(Integer, nullable=False, unique=False, default=0)
    guests_did_vote_count = Column(Integer, nullable=False, unique=False, default=0)
    current_votes = Column(ARRAY(Integer), nullable=True, default=[0])
    votes = Column(Text, nullable=True, default="0")

    def __init__(self, room_id: int):
        self.room_id = room_id

    def __repr__(self):
        return f"<room_id = {self.room_id}, guest_count = {self.guest_count}>"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "guest_count": self.guest_count,
            "guests_did_vote_count": self.guests_did_vote_count,
            "current_votes": self.current_votes,
            "votes": self.votes
        }


# FAT MODEL WITH SESSION

session = SessionLocal()


async def delete_room_by_id(room: RoomSchema):
    try:
        session.query(Room).filter(Room.room_id == room.room_id).delete()
        session.commit()
    except exc.SQLAlchemyError as ex:
        session.rollback()
        raise ex


async def create_room_dto():
    new_room_dto = Room(random.randint(999, 9999))
    try:
        session.add(new_room_dto)
        session.commit()
        return new_room_dto.serialize
    except exc.SQLAlchemyError as ex:
        session.rollback()
        raise ex


async def join_room_with_id(_id):
    try:
        session.query(Room).filter(Room.room_id == _id).update({Room.guest_count: Room.guest_count + 1})
        session.commit()
    except exc.SQLAlchemyError as ex:
        raise ex


async def add_room_votes(room_id, votes: VoteSchema):
    try:
        dbo = session.query(Room).filter(Room.room_id == room_id)

        for database_object in dbo:
            obj = database_object.serialize
            updated_room_object = {
                **obj,
                "current_votes": obj["current_votes"] + "," + f"{votes.votes}",
                "guests_did_vote_count": obj["guests_did_vote_count"] + 1
            }
            dbo.update(updated_room_object)
            session.commit()

    except exc.SQLAlchemyError as ex:
        raise ex


async def refresh_voting_session(room_dbo):
    try:
        room_dbo.update({Room.current_votes: "0"})
        room_dbo.update({Room.guests_did_vote_count: 0})

        session.commit()

    except exc.SQLAlchemyError as ex:
        raise ex


async def end_voting_session():
    pass
