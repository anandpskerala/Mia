from typing import Union, List
from pydantic import BaseModel
from mia.database import MDB

filter_collection = MDB().db.filters


class Filters(BaseModel):
    chat_id: str
    trigger: str
    message_id: str
    alerts: Union[List, str, None]


def get_all_filters(chat_id: str):
    filters = []
    raw_data = filter_collection.find({"chat_id": chat_id})
    for data in raw_data:
        filters.append(Filters(**data))
    return filters


def add_filter(chat_id: str, trigger: str, message_id: str, alerts: Union[str, List, None]):
    if filter_collection.find_one({"chat_id": chat_id, "trigger": trigger}) is not None:
        filter_collection.update_one(
            {"chat_id": chat_id, "trigger": trigger},
            {"$set": {"message_id": message_id, "alerts": alerts}}
        )
    else:
        filter_collection.insert_one(
            {
                "chat_id": chat_id,
                "trigger": trigger,
                "message_id": message_id,
                "alerts": alerts
            }
        )


def count_filters(chat_id: str):
    return filter_collection.count_documents({"chat_id": chat_id})


def delete_filter(chat_id: str, trigger: str):
    filter_collection.delete_one(
        {
            "chat_id": chat_id,
            "trigger": trigger
        }
    )


def delete_all_filters(chat_id: str):
    filter_collection.delete_many({"chat_id": chat_id})


def find_filter_one(chat_id: str, trigger: str):
    data = filter_collection.find_one(
        {
            "chat_id": chat_id,
            "trigger": trigger
        }
    )

    return Filters(**data)
