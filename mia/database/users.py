from mia.database import MDB

user_collection = MDB().db.users


def insert_user(user_id: str, user_name: str, dc_id: str):
    if user_collection.count_documents({"_id": user_id}) > 0:
        return False
    else:
        user_collection.insert_one(
            {
                "_id": user_id,
                "user_name": user_name,
                "dc_id": dc_id
            }
        )


def get_user(user_id: str):
    return user_collection.find_one({"_id": user_id})
