from src.common.database import Database
import src.models.users.errors as UserErrors
from flask import session, flash
from src.common.utils import Utils


class User(object):
    def __init__(self, email, password, fName, age):
        self.email = email
        self.password = password
        self.fName = fName
        self.age = age
        self.port_ids = []
        
    def json(self):
        return {
            "email": self.email,
            "password": self.password,
            "fName": self.fName,
            "age": self.age,
            "port_ids": self.port_ids            
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())

    @staticmethod
    def register_user(email, password, fName, age):
        user_data = User.get_by_email(email)
        if user_data is not None:
            raise UserErrors.UserAlreadyRegisteredError("You already have an account with this email address.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("This is an invalid email address!")

        User(email, Utils.hash_password(password), fName, age).save_to_mongo()
        return True

    @staticmethod
    def get_by_email(email):
        data = Database.find_one(collection="users", query={"email": email})
        if data is not None:
            return data
        else:
            return None

    @staticmethod
    def login_valid(email, password):
        user_data = User.get_by_email(email)
        if user_data is None:
            # Tell the user their email does not exist
            raise UserErrors.UserNotExistsError("This account does not exist!")
        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell the user their password is wrong
            raise UserErrors.IncorrectPasswordError("Your password was wrong!")
        return True


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

    @staticmethod
    def add_portfolio_to_user(email, port_id):
        user = User.get_by_email(email)
        user["port_ids"].append(port_id)
        Database.update("users",{"email": user["email"]},
                        {"email": user["email"], "password": user['password'], "fName": user['fName'], "age": user['age'], "port_ids": user["port_ids"]})

    @staticmethod
    def get_port_ids(email):
        user = User.get_by_email(email)
        if user is not None:
            return user["port_ids"]
        else:
            return None

    @staticmethod
    def change_password(email, new_pass):
        user = User.get_by_email(email)
        Database.update("users",{"email": user["email"]},
                        {"email": user["email"], "password": Utils.hash_password(new_pass), "fName": user['fName'], "age": user['age'], "port_ids": user["port_ids"]})
        flash("Successfully Changed Password!")
