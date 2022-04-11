from pydantic import BaseModel
from mia.database import MDB

user_collection = MDB().db.users


class Users(BaseModel):
    user_id: str
    user_name: str
    dc_id: str


def insert_user(user_id: str, user_name: str, dc_id: str):
    if user_collection.find_one({"user_id": user_id}) is not None:
        return False
    else:
        user_collection.insert_one(
            {
                "user_id": user_id,
                "user_name": user_name,
                "dc_id": dc_id
            }
        )


def get_user(user_id: str):
    return Users(**user_collection.find_one({"user_id": user_id}))
