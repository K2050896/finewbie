import pymongo
import os

class Database(object):
    URI = os.environ.get("MONGODB_URI")
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["Capstone"]

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def delete_all(collection, query):
        Database.DATABASE[collection].remove(query)

    @staticmethod
    def update(collection,document,query):
        Database.DATABASE[collection].update(document,query)
