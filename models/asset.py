from common.database import Database

class Asset(object):
    def __init__(self, id, port_id):
        self.id = id # 1-6 ( each assets )
        self.port_id = port_id #portfolio id
        self.returns = []


    def json(self):
        return {
            "id": self.id,
            "port_id": self.port_id,
            "returns": self.returns
        }

    def save_to_mongo(self):
        Database.insert("assets", self.json())

    @classmethod
    def from_mongo(cls, port_id):
        return [asset for asset in Database.find(collection='assets', query={'port_id': port_id})]

    @staticmethod
    def delete_all_assets(port_id):
        Database.delete_all(collection='assets', query={"port_id": port_id})



