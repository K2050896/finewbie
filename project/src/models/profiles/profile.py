from src.common.database import Database
from src.models.users.user import User
from src.models.portfolios.portfolio import Portfolio

class Profile(object):
    def __init__(self, port_id, user_email, name, horizon, time_left, dis_inc, init_con, goal, importance, r1, r2, r3, r4, r5):
        self.port_id = port_id
        self.user_email = user_email
        self.name = name
        
        # Adding portfolio ID into users document
        User.add_portfolio_to_user(user_email, port_id)
        
        # Creating new Porfolio Document
        new = Portfolio(port_id, user_email, name, [],[],[],[],[],[],[],[],[],[],[])
        new.save_to_mongo()
        
        self.horizon = horizon
        self.time_left = float(time_left)
        self.dis_inc = dis_inc
        self.init_con = float(init_con)
        self.importance = importance
        self.goal = float(goal)
        
        if self.horizon[-1] <= 1:
            t = 1
        elif self.horizon[-1] <=2:
            t = 2
        elif self.horizon[-1] <= 5:
            t = 3
        elif self.horizon[-1] <= 10:
            t = 4
        else:
            t = 5
        
        time = (6 - int(importance) + t)/2
        risk = (int(r1)+int(r2)+int(r3)+int(r4)+int(r5))*2
        
        if time <= 1:
            if risk <= 18:
                profile = "Conservative"
            elif risk <= 31:
                profile = "Moderately Conservative"
            else:
                profile = "Moderate"
                
        elif time <= 2:
            if risk <= 15:
                profile = "Conservative"
            elif risk <= 24:
                profile = "Moderately Conservative"
            elif risk <= 35:
                profile = "Moderate"
            else:
                profile = "Moderately Aggressive"
                
        elif time <= 3:
            if risk <= 12:
                profile = "Conservative"
            elif risk <= 20:
                profile = "Moderately Conservative"
            elif risk <= 28:
                profile = "Moderate"
            elif risk <= 37:
                profile = "Moderately Aggressive"
            else:
                profile = "Aggressive"
        
        elif time <= 4:
            if risk <= 11:
                profile = "Conservative"
            elif risk <= 18:
                profile = "Moderately Conservative"
            elif risk <= 25:
                profile = "Moderate"
            elif risk <= 34:
                profile = "Moderately Aggressive"
            else:
                profile = "Aggressive"
                
        else:
            if risk <= 10:
                profile = "Conservative"
            elif risk <= 17:
                profile = "Moderately Conservative"
            elif risk <= 24:
                profile = "Moderate"
            elif risk <= 31:
                profile = "Moderately Aggressive"
            else:
                profile = "Aggressive"
        
        if profile == "Conservative":
            self.init_alloc = [0.15,0,0.05,0.25,0.25,0.3]
            self.lamb = 1.00
        elif profile == "Moderately Conservative":
            self.init_alloc = [0.25,0.05,0.10,0.25,0.25,0.10]
            self.lamb = 0.75
        elif profile == "Moderate":
            self.init_alloc = [0.35,0.10,0.15,0.175,0.175,0.05]
            self.lamb = 0.50
        elif profile == "Moderately Aggressive":
            self.init_alloc = [0.45,0.15,0.20,0.075,0.075,0.05]
            self.lamb = 0.25
        else:
            self.init_alloc = [0.50,0.20,0.25,0,0,0.05]
            self.lamb = 0.00

    def json(self):
        return {
            "port_id": self.port_id,
            "user_email": self.user_email,
            "name": self.name,
            "goal": self.goal,
            "horizon": self.horizon,
            "time_left": self.time_left,
            "init_con": self.init_con,
            "dis_inc": self.dis_inc,
            "init_alloc": self.init_alloc,
            "lamb": self.lamb,
            "importance": self.importance
        }

    def save_to_mongo(self):
        Database.insert("profiles", self.json())

   
    @staticmethod
    def from_mongo(port_id):
        data = Database.find_one(collection="profiles", query={'port_id': port_id})
        if data is not None:
            return data
        else:
            return None

    @staticmethod
    def delete_profile(port_id):
        Database.delete_all(collection="profiles", query ={"port_id": port_id})
   
    @staticmethod
    def update_profile(port_id, query):
        # query must include all the fields of profiles
        Database.update("profiles", {"port_id": port_id}, query)

    @staticmethod
    def find_user(port_id):
        data = Profile.from_mongo(port_id)
        if data is not None:
            return data["user_email"]
        else:
            return None
