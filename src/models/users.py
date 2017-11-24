from common.database import Database
from flask import session


class User(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.port_ids = []

    def json(self):
        return {
            "email": self.email,
            "password": self.password,
            "port_ids": self.port_ids
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())

    @classmethod
    def register_user(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False

    @staticmethod
    def get_by_email(email):
        data = Database.find_one(collection="users", query={"email": email})
        if data is not None:
            return data

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user['password'] == password
        return False


    @staticmethod
    def login(user_email):
        # login_valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    @staticmethod
    def delete_user(user_email):
        Database.delete_all(collection='users', query ={"email": user_email})

    def add_portfolio(self, port_id):
        self.port_ids.append(port_id)