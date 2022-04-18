from typing import Union, List, Optional
from pydantic import BaseModel
from mia.database import MDB

welcome_collection = MDB().db.welcome


class Welcome(BaseModel):
    chat_id: Optional[str]  # Made all elements optional to avoid further complications
    message_id: Optional[str]
    no_format: Optional[str]
    state: Optional[bool]
    clean_welcome: Optional[bool]
    clean_service: Optional[bool]
    previous_welcome: Optional[str]
    alerts: Optional[Union[List, None]]


def add_welcome_strings(chat_id: str, msg_id: str, alerts: Union[List, None], state: bool, no_format: str):
    if welcome_collection.find_one({"chat_id": chat_id}) is not None:
        welcome_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"message_id": msg_id, "alerts": alerts, "state": state, "no_format": no_format}}
        )
    else:
        welcome_collection.insert_one(
            {
                "chat_id": chat_id,
                "message_id": msg_id,
                "alerts": alerts,
                "state": state,
                "no_format": no_format
            }
        )


def set_previous_welcome(chat_id: str, msg_id: str):
    if welcome_collection.find_one({"chat_id": chat_id}) is not None:
        welcome_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"previous_welcome": msg_id}}
        )
    else:
        welcome_collection.insert_one(
            {
                "chat_id": chat_id,
                "previous_welcome": msg_id
            }
        )


def get_welcome(chat_id: str):
    data = welcome_collection.find_one(
        {"chat_id": chat_id}
    )

    return Welcome(**data) if data is not None else None


def set_clean_welcome(chat_id: str, state: bool):
    if welcome_collection.find_one({"chat_id": chat_id}) is not None:
        welcome_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"clean_welcome": state}}
        )
    else:
        welcome_collection.insert_one(
            {
                "chat_id": chat_id,
                "clean_welcome": state
            }
        )


def set_clean_service(chat_id: str, state: bool):
    if welcome_collection.find_one({"chat_id": chat_id}) is not None:
        welcome_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"clean_service": state}}
        )
    else:
        welcome_collection.insert_one(
            {
                "chat_id": chat_id,
                "clean_service": state
            }
        )


def set_welcome_state(chat_id: str, state: bool):
    if welcome_collection.find_one({"chat_id": chat_id}) is not None:
        welcome_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"state": state}}
        )
    else:
        welcome_collection.insert_one(
            {
                "chat_id": chat_id,
                "state": state
            }
        )


def reset_welcome(chat_id: str):
    if welcome_collection.find_one({"chat_id": chat_id}) is not None:
        welcome_collection.delete_one(
            {
                "chat_id": chat_id
            }
        )
