from mia import CONFIG
from mia.database import MDB

lang_collection = MDB().db.langs


def update_lang(chat_id: str, lang: str):
    if lang_collection.count_documents({"_id": chat_id}) > 0:
        lang_collection.update_one(
            {"_id": chat_id},
            {"$set": {"lang": lang}}
        )
    else:
        lang_collection.insert_one(
            {
                "_id": chat_id,
                "lang": lang
            }
        )


def get_lang_code(chat_id: str):
    result = lang_collection.find_one({"_id": chat_id})
    return result.get("lang") if result is not None else CONFIG.default_lang
