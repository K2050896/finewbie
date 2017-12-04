import uuid
import numpy as np
import pandas as pd
plt.style.use('ggplot')
from src.common.database import Database
import src.models.portfolios.constants as cnst


class Portfolio(object):
    def __init__(self, port_id, user_email, name, mean_term_wealth, mean_var_wealth, alloc_percent, shares0, shares1, cont, reached, reached_dollar, hprr, twrr, ambitious):
        self.port_id = port_id
        self.user_email = user_email
        self.name = name
        self.mean_term_wealth = mean_term_wealth
        self.mean_var_wealth = mean_var_wealth
        self.alloc_percent = alloc_percent
        self.shares0 = shares0
        self.shares1 = shares1
        self.cont = cont
        self.reached = reached
        self.reached_dollar = reached_dollar
        self.hprr = hprr
        self.twrr = twrr
        self.ambitious = ambitious
        
        
    def json(self):
        return {
            "port_id": self.port_id,
            "user_email": self.user_email,
            "name": self.name,
            "mean_term_wealth": self.mean_term_wealth,
            "mean_var_wealth": self.mean_var_wealth,
            "alloc_percent": self.alloc_percent,
            "shares0": self.shares0,
            "shares1": self.shares1,
            "cont": self.cont,
            "reached": self.reached,
            "reached_dollar": self.reached_dollar,
            "hprr": self.hprr,
            "twrr": self.twrr,
            "ambitious": self.ambitious
        }

    def save_to_mongo(self):
        Database.insert("portfolios", self.json())

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

    # @staticmethod
    # def plot_portfolio(Portfolio):
    #     fig = plt.figure(figsize=(12, 6))
    #     ax = fig.add_subplot(111)
    #     plt.pie(Portfolio['alloc_percent'][-1], labels=['SPY', 'IWM', 'VEU', 'CSJ', 'BLV', 'Cash Inv'], autopct='%1.1f%%')
    #     return fig
