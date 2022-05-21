from operator import itemgetter

from app.data_sources.cache import redis_client
from app.models.room import create_room_dto
from app.schemas.vote import VoteSchema


async def create_and_cache_room():
    room = await create_room_dto()

    redis_client.set(room["room_id"], room)

    return {
        "id": room["id"],
        "room_id": room["room_id"],
    }


def join_room_by_id(room_id):
    room = redis_client.get(room_id)

    updated_room = {
        **room,
        "guest_count": room["guest_count"] + 1
    }

    redis_client.set(room_id, updated_room)

    return {
        "id": updated_room["id"],
        "room_id": updated_room["room_id"],
        "guest_count": updated_room["guest_count"]
    }


def add_session_votes_by_room_id(room_id, req_body: VoteSchema):
    room = redis_client.get(room_id)

    updated_room = {
        **room,
        "current_votes": room["current_votes"] + req_body.votes,
    }

    redis_client.set(room_id, updated_room)

    return {
        "id": updated_room["id"],
        "room_id": updated_room["room_id"],
        "guest_count": updated_room["guest_count"]
    }


def end_voting_session_and_return_voted_value(room_id):
    room = redis_client.get(room_id)

    grouped_votes = []
    for vote in set(room["current_votes"][1:]):
        grouped_votes.append({"vote": vote, "occurrences": room["current_votes"].count(vote)})

    sorted_votes = sorted(grouped_votes, key=itemgetter("occurrences"), reverse=True)

    updated_room = {
        **room,
        "current_votes": [0],
    }

    # redis_client.set(room_id,updated_room)

    return {
        "id": updated_room["id"],
        "room_id": updated_room["room_id"],
        "voted_value": sorted_votes
    }
