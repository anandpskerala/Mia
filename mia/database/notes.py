from typing import Union, List
from pydantic import BaseModel
from mia.database import MDB

note_collection = MDB().db.notes


class Notes(BaseModel):
    chat_id: str
    trigger: str
    message_id: str
    alerts: Union[List, str, None]


def get_all_notes(chat_id: str):
    notes = []
    raw_data = note_collection.find({"chat_id": chat_id})
    for data in raw_data:
        notes.append(Notes(**data))
    return notes


def add_note(chat_id: str, trigger: str, message_id: str, alerts: Union[str, List, None]):
    if note_collection.find_one({"chat_id": chat_id, "trigger": trigger}) is not None:
        note_collection.update_one(
            {"chat_id": chat_id, "trigger": trigger},
            {"$set": {"message_id": message_id, "alerts": alerts}}
        )
    else:
        note_collection.insert_one(
            {
                "chat_id": chat_id,
                "trigger": trigger,
                "message_id": message_id,
                "alerts": alerts
            }
        )


def count_notes(chat_id: str):
    return note_collection.count_documents({"chat_id": chat_id})


def delete_note(chat_id: str, trigger: str):
    note_collection.delete_one(
        {
            "chat_id": chat_id,
            "trigger": trigger
        }
    )


def delete_all_notes(chat_id: str):
    note_collection.delete_many({"chat_id": chat_id})


def find_one_note(chat_id: str, trigger: str):
    data = note_collection.find_one(
        {
            "chat_id": chat_id,
            "trigger": trigger
        }
    )

    return Notes(**data) if data is not None else None
