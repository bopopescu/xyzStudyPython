# -*- coding: utf-8 -*-
"""
mongo client
"""
from pymongo import MongoClient

MONGODB_URL = 'mongodb://localhost:27017'
DB_NAME = 'fang_price'


class Mixin(object):
    """
    mongo client
    """
    _client = None

    def __init__(self):
        if not self._client:
            self._client = MongoClient(MONGODB_URL)

    @property
    def db(self):
        if self._client:
            return self._client[DB_NAME]
        else:
            self._client = MongoClient(MONGODB_URL)
            return self.db

if __name__ == "__main__":
    m = Mixin()
    m.db.fang_price.insert({"asdf": None, "dsf": "dsfdsf"})
    pass