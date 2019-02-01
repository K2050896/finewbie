import pymongo
import os

class Database(object):
    URI = os.environ.get("MONGODB_URI") # "mongodb://127.0.0.1:27017" for local
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["heroku_g0lnhdnb"] #"fullstack" for local

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
