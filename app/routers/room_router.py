from fastapi import APIRouter

from app.api_helpers.room_helper import create_and_cache_room, join_room_by_id, add_session_votes_by_room_id, \
    end_voting_session_and_return_voted_value
from app.models.room import delete_room_by_id
from app.schemas.room import RoomSchema
from app.schemas.vote import VoteSchema

room_router = APIRouter()


@room_router.get("/")
async def default():
    return {"Hello": "World"}


@room_router.get("/test")
async def test():
    return {}


@room_router.delete("/deleteroom")
async def delete_room(room: RoomSchema):
    await delete_room_by_id(room)
    return room


@room_router.get("/createroom")
async def create_room():
    return await create_and_cache_room()


@room_router.post("/room/{room_id}")
async def join_room(room_id: int):
    return join_room_by_id(room_id)


@room_router.post("/room/{room_id}/vote")
async def room_vote(room_id: int, req_body: VoteSchema):
    return add_session_votes_by_room_id(room_id, req_body)


@room_router.get("/room/{room_id}/vote/end")
async def end_voting_session(room_id: int):
    return end_voting_session_and_return_voted_value(room_id)
