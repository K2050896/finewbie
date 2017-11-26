from src.common.database import Database

class Setting(object):
    def __init__(self, id, port_id, name, Y,T , dis_inc, init_con, goal, t1, t2, r1, r2, r3, r4):
        #T1 is the time horizon 
        self.port_id = port_id #portfolio id
        self.name = name
        self.Y = Y
        self.T = T
        if length <= 1:
            t = 1
        if length > 1 and <=2:
            t = 2
        elif length > 2 and length <= 5:
            t = 3
        elif length > 5 and length <= 10:
            t = 4
        elif length > 10:
            t = 5
        
        (6 - importance + t)/2 = time
        r = r1+ r2+ r3+ r4
        
        self.lamb
        self.init_alloc = 
        
        
        
        self.dis_inc = dis_inc
        self.init_con = init_con
        self.goal = goal


    def json(self):
        return {
            "port_id": self.port_id,
            "name": self.name,
            "length remaining": self.T,
            "lamb": self.lamb,
            "dis_inc": self.dis_inc,
            "init_con": self.init_con,
            "init_alloc": self.init_alloc
            "goal": self.goal
            
        }

    def save_to_mongo(self):
        Database.insert("settings", self.json())

   
    @staticmethod
    def from_mongo(port_id):
        data = Database.find_one(collection='settings', query={'port_id': port_id})
        if data is not None:
            return data

    @staticmethod
    def delete_setting(port_id):
        Database.delete_all(collection='settings', query ={"port_id": port_id})
    
    @staticmethod
    def convert_setting(settings):
        name = setting[0] # string
        length = setting[1] # float
        budget = setting[2] # int
        importance = setting[3] # 1-5
        initial_contribution = setting[5] #int
        value_assets = setting[6] #int
        value_liabilities = setting[7] #int
        risk1 = setting[8] # 1-4
        risk2 = setting[9] # 1-4
        risk3 = setting[10] # 1-4
        risk4 = setting[11] # 1-4
        risk5 = setting[12] # 1-4
        
        risk = (risk1 + risk2 + risk3 + risk4 + risk5) * 2 
        
        if length <= 1:
            t = 1
        if length > 1 and <=2:
            t = 2
        elif length > 2 and length <= 5:
            t = 3
        elif length > 5 and length <= 10:
            t = 4
        elif length > 10:
            t = 5
        
        (6 - importance + t)/2 = time
        
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
                profile = "Conservative:
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
        return name, profile
        
        
        
