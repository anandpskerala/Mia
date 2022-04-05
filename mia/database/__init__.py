from pymongo import MongoClient

from mia import CONFIG


class MDB:
    def __init__(self):
        self.client = MongoClient(
            CONFIG.database_url
        )

        self.db = self.client['mia']
