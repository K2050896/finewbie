from src.common.database import Database

class Profile(object):
    def __init__(self, id, port_id, name, Y, T , dis_inc, init_con, goal, importance, r1, r2, r3, r4):
        self.port_id = port_id #portfolio id
        self.name = name
        self.Y = Y
        self.T = T
        self.dis_inc = dis_inc
        self.init_con = init_con
        self.goal = goal
        
        if Y <= 1:
            t = 1
        if Y > 1 and Y <=2:
            t = 2
        elif Y > 2 and Y <= 5:
            t = 3
        elif Y > 5 and Y <= 10:
            t = 4
        elif Y > 10:
            t = 5
        
        time = (6 - importance + t)/2 
        risk = (r1+ r2+ r3+ r4)*2
        
        if time > 0 and time <= 1:
            if risk > 0 and risk <= 18:
                profile = "Conservative"
            elif risk > 18 and risk <= 31:
                profile = "Moderately Conservative"
            elif risk > 31 and risk <= 40:
                profile = "Moderate"
                
        elif time > 1 and time <= 2:
            if risk > 0 and risk <= 15:
                profile = "Conservative"
            elif risk > 15 and risk <= 24:
                profile = "Moderately Conservative"
            elif risk > 24 and risk <= 35:
                profile = "Moderate"
            elif risk > 35 and risk <= 40:
                profile = "Moderately Aggressive"
                
        elif time > 2 and time <= 3:
            if risk > 0 and risk <= 12:
                profile = "Conservative"
            elif risk > 12 and risk <= 20:
                profile = "Moderately Conservative"
            elif risk > 20 and risk <= 28:
                profile = "Moderate"
            elif risk > 28 and risk <= 37:
                profile = "Moderately Aggressive"
            elif risk > 37 and risk <= 40:
                profile = "Aggressive"
        
        elif time > 3 and time <= 4:
            if risk > 0 and risk <= 11:
                profile = "Conservative"
            elif risk > 11 and risk <= 18:
                profile = "Moderately Conservative"
            elif risk > 18 and risk <= 25:
                profile = "Moderate"
            elif risk > 25 and risk <= 34:
                profile = "Moderately Aggressive"
            elif risk > 34 and risk <= 40:
                profile = "Aggressive"
                
        elif time > 4 and time <= 5:
            if risk > 0 and risk <= 10:
                profile = "Conservative"
            elif risk > 10 and risk <= 17:
                profile = "Moderately Conservative"
            elif risk > 17 and risk <= 24:
                profile = "Moderate"
            elif risk > 24 and risk <= 31:
                profile = "Moderately Aggressive"
            elif risk > 31 and risk <= 40:
                profile = "Aggressive"
        
        if profile == "Conservative":
            self.init_alloc = [0.15,0,0.05,0.25,0.25,0.3]
            self.lamb = 0.00
        elif profile == "Moderately Conservative":
            self.init_alloc = [0.25,0.05,0.10,0.25,0.25,0.10]
            self.lamb = 0.25
        elif profile == "Moderate":
            self.init_alloc = [0.35,0.10,0.15,0.175,0.175,0.05]
            self.lamb = 0.50
        elif profile == "Moderately Aggressive":
            self.init_alloc = [0.45,0.15,0.20,0.075,0.075,0.05]
            self.lamb = 0.75
        elif profile == "Aggressive":
            self.init_alloc = [0.50,0.20,0.25,0,0,0.05]
            self.lamb = 1.00
            



    def json(self):
        return {
            "port_id": self.port_id,
            "name": self.name,
            "time_horizon": self.Y,
            "time_left": self.T,
            "lamb": self.lamb,
            "dis_inc": self.dis_inc,
            "init_con": self.init_con,
            "init_alloc": self.init_alloc,
            "goal": self.goal
        }

    def save_to_mongo(self):
        Database.insert("profiles", self.json())

   
    @staticmethod
    def from_mongo(port_id):
        data = Database.find_one(collection='profiles', query={'port_id': port_id})
        if data is not None:
            return data

    @staticmethod
    def delete_profile(port_id):
        Database.delete_all(collection='profiles', query ={"port_id": port_id})
   
    @staticmethod
    def update_profile(port_id, query):
        # query must include all the fields of profiles
        Database.update("profiles",{"port_id": port_id},
                        query)
