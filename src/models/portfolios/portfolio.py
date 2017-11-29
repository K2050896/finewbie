import uuid
from src.common.database import Database


class Portfolio(object):
    def __init__(self, user_email, port_id):
        self.port_id = port_id
        self.user_email = user_email
        self.mean_term_wealth = mean_term_wealth
        self.mean_var_wealth = mean_var_wealth
        self.alloc_percent = alloc_percent
        self.shares0 = shares0
        self.shares1 = shares1
        self.cont = cont
        self.reached = reached
        self.ambitious = ambitious
        
        
    def json(self):
        return {
            "port_id": self.port_id,
            "mean_term_wealth": self.mean_term_wealth,
            "mean_var_wealth": self.mean_var_wealth,
            "alloc_percent": self.alloc_percent,
            "shares0": self.shares0,
            "shares1": self.shares1,
            "cont": self.cont,
            "reached": self.reached,
            "ambitious": self.ambitious
        }

    def save_to_mongo(self):
        Database.insert("portfolios", self.json())

    #@classmethod
    @staticmethod
    def from_mongo(port_id):
        port_data = Database.find_one(collection='portfolios', query={'port_id': port_id})
        if port_data is not None:
            return port_data

    @staticmethod
    def delete_portfolio(port_id):
        Database.delete_all(collection='portfolios', query={"port_id": port_id})
        
    @staticmethod
    def update_portfolio(port_id, query):
        # query must include all the fields of profiles
        Database.update("portfolios", {"port_id": port_id},
                        query)
    '''
    @staticmethod
    def update_shares(port_id, new_shares):
        port = Portfolio.from_mongo(port_id)
        Portfolio.update_portfolio(port_id,
                                   {
                                    "port_id": port_id,
                                    "mean_term_wealth": port["mean_term_wealth"],
                                    "mean_var_wealth": port["mean_var_wealth"],
                                    "alloc_percent": port["alloc_percent"],
                                    "shares": new_shares,
                                    "cont": port["cont"],
                                    "reached": port["reached"],
                                    "ambitious": port["ambitious"]
                                  } )
                                   
   '''
