from src.common.database import Database

class Setting(object):
    def __init__(self, id, port_id, settings):
        self.port_id = port_id #portfolio id
        self.settings = settings


    def json(self):
        return {
            "port_id": self.port_id,
            "settings": self.settings
        }

    def save_to_mongo(self):
        Database.insert("settings", self.json())

    @classmethod
    def from_mongo(cls, port_id):
        return [asset for asset in Database.find(collection='settings', query={'port_id': port_id})]

    @staticmethod
    def delete_setting(port_id):
        Database.delete_all(collection='settings', query ={"port_id": port_id})

