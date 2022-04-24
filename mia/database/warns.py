from typing import List, Optional, Union
from pydantic import BaseModel, Field
from mia.database import MDB

warns_collection = MDB().db.warns
warn_filters_collection = MDB().db.warn_filters
warn_settings_collection = MDB().db.warn_settings


class Warns(BaseModel):
    chat_id: str
    user_id: str
    reason: Optional[List[str]]
    num_warns: str


class WarnFilters(BaseModel):
    chat_id: str
    trigger: str
    reply: str


class WarnSettings(BaseModel):
    chat_id: str
    limit: Optional[str] = Field(default="3")


def add_user_warn(chat_id: str, user_id: str, reason: Union[str, None]):
    warns = warns_collection.find_one({"chat_id": chat_id, "user_id": user_id})
    if warns:
        warn_limit = int(warns["num_warns"]) + 1
        if reason:
            if warns.get('reason'):
                reasons = warns['reason'].append(reason)
            else:
                reasons = [reason]
            warns_collection.update_one(
                {"chat_id": chat_id, "user_id": user_id},
                {"$set": {"num_warns": str(warn_limit), "reason": reasons}},
            )
        else:
            warns_collection.update_one(
                {"chat_id": chat_id, "user_id": user_id},
                {"$set": {"num_warns": str(warn_limit)}}
            )
    else:
        warn_limit = 1
        if reason:
            warns_collection.insert_one(
                {
                    "chat_id": chat_id,
                    "user_id": user_id,
                    "reason": [reason],
                    "num_warns": str(warn_limit)
                }
            )
        else:
            warns_collection.insert_one(
                {
                    "chat_id": chat_id,
                    "user_id": user_id,
                    "num_warns": str(warn_limit)
                }
            )
    return warn_limit


def get_warnings(chat_id: str, user_id: str):
    warns = warns_collection.find_one({"chat_id": chat_id, "user_id": user_id})
    return Warns(**warns) if warns else None


def change_warn_settings(chat_id: str, limit: str):
    if warn_settings_collection.find_one({"chat_id": chat_id}):
        warn_settings_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"limit": limit}}
        )
    else:
        warn_settings_collection.insert_one(
            {
                "chat_id": chat_id,
                "limit": limit
            }
        )


def get_warn_settings(chat_id: str):
    data = warn_settings_collection.find_one({"chat_id": chat_id})
    return WarnSettings(**data) if data else None


def add_warn_filter(chat_id: str, trigger: str, reply: str):
    if warn_filters_collection.find_one({"chat_id": chat_id, "trigger": trigger}):
        warn_filters_collection.update_one(
            {"chat_id": chat_id, "trigger": trigger},
            {"$set": {"reply": reply}}
        )
    else:
        warn_filters_collection.insert_one(
            {
                "chat_id": chat_id,
                "trigger": trigger,
                "reply": reply
            }
        )


def get_all_warn_filters(chat_id: str):
    filters = []
    raw_data = warn_filters_collection.find({"chat_id": chat_id})
    for data in raw_data:
        filters.append(WarnFilters(**data))

    return filters


def remove_last_warn(chat_id: str, user_id: str):
    warns = warns_collection.find_one({"chat_id": chat_id, "user_id": user_id})
    if warns:
        if warns.get('reason'):
            reasons = warns['reason'].pop(-1)
        else:
            reasons = []
        warns_collection.update_one(
            {"chat_id": chat_id, "user_id": user_id},
            {"$set": {"num_warns": str(int(warns['num_warns']) - 1), "reason": reasons}},
        )


def reset_all_warns(chat_id: str, user_id: str):
    warns = warns_collection.find_one({"chat_id": chat_id, "user_id": user_id})
    if warns:
        warns_collection.update_one(
            {"chat_id": chat_id, "user_id": user_id},
            {"$set": {"num_warns": str(0), "reason": []}}
        )
