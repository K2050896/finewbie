from flask import Blueprint

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login')
def login_user():
    pass

@user_blueprint.route('/logout')
def logout_user():
    pass