from fastapi import APIRouter

from app.models.user import create_user_dto
from app.schemas.user import UserSchema

user_router = APIRouter()


@user_router.post("/createuser")
def create_user(user: UserSchema):
    response = create_user_dto(user)
    return response


@user_router.delete("/deleteuser")
def delete_user_by_id(user: UserSchema):
    response = delete_user_by_id(user)
    return response
