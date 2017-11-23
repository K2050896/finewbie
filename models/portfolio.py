import uuid
from common.database import Database


class Portfolio(object):
    def __init__(self,port_id=None):
        self.port_id = uuid.uuid4().hex if port_id is None else port_id
        self.time_series = []
        # self.time_len = function of time series depending on the organization of the data

    def json(self):
        return {
            "port_id": self.port_id,
            "time_series": self.time_series
        }

    def save_to_mongo(self):
        Database.insert("portfolios", self.json())

    #@classmethod
    @staticmethod
    def from_mongo(port_id):
        port_data = Database.find_one(collection='portfolios', query={'port_id': port_id})
        if port_data is not None:
            return (port_data)

    @staticmethod
    def delete_portfolio(port_id):
        Database.delete_all(collection='portfolios', query={"port_id": port_id})
