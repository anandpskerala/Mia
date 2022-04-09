from typing import Union, List
from pydantic import BaseModel
from mia.database import MDB

filter_collection = MDB().db.filters


class Filters(BaseModel):
    chat_id: str
    trigger: str
    message_id: str
    alerts: Union[List, None]
