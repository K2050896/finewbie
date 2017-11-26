from src.common.database import Database

class Share(object):
    def __init__(self, id, port_id, shares):
        self.port_id = port_id #portfolio id
        self.shares = shares


    def json(self):
        return {
            "port_id": self.port_id,
            "shares": self.shares
        }

    def save_to_mongo(self):
        Database.insert("shares", self.json())


    @staticmethod
    def from_mongo(port_id):
        setting = Database.find_one(collection='settings', query={'port_id': port_id})
        if setting is not None:
            return (setting)

    @staticmethod
    def delete_shares(port_id):
        Database.delete_all(collection='shares', query ={"port_id": port_id})

    @staticmethod
    def update_shares(port_id, shares):
        Database.update("shares", {"port_id": port_id},
                        {"port_id": port_id, "shares": shares})

'''
from src.models.share import Share
share = Share(portfolio_id)

'''