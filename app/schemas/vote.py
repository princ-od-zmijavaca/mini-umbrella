from pydantic import BaseModel
from typing import List


class VoteSchema(BaseModel):
    votes: List[int]
