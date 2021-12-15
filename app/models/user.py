from .database import Base, SessionLocal
from sqlalchemy import Integer, Column, String, exc

from ..schemas.user import UserSchema


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"<room_id = {self.name}>"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


# FAT MODEL WITH SESSION


session = SessionLocal()


def create_user_dto(user: UserSchema):
    new_user_dto = User(user.id, user.name)
    session.add(new_user_dto)
    session.commit()
    return new_user_dto.serialize


def delete_user_by_id(user: UserSchema):
    try:
        session.query(User).filter(User.id == user.id).delete()
        session.commit()
    except exc.SQLAlchemyError as ex:
        print(type(ex))
    finally:
        return user.id
