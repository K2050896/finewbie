from flask import Blueprint, request, render_template, session, redirect, url_for
from src.models.users.user import User
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        try:
            if User.login_valid(email, password):
                User.login(email)
                return redirect(url_for(".user_homepage"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/login.jinja2")

@user_blueprint.route('/register', methods = ['GET','POST'])
def register_user():   # Views form required for user signup
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fName = request.form['fName']
        age = request.form['age']
        try:
            if User.register_user(email, password, fName, age):
                session['email'] = email
                return redirect(url_for(".user_homepage"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/register.jinja2")

@user_blueprint.route('/logout')
def logout_user():
    User.logout()
    return render_template("users/logout.jinja2")

@user_blueprint.route('/homepage')
@user_decorators.requires_login
def user_homepage():
    return render_template("homepage.jinja2", email=session['email'])

@user_blueprint.route('/my-info')
@user_decorators.requires_login
def my_info():
    return render_template("my_info.jinja2")

@user_blueprint.route('/faqs')
@user_decorators.requires_login
def faqs():
    return render_template("resources.jinja2")

@user_blueprint.route('/assets')
@user_decorators.requires_login
def assets():
    return render_template("resources.jinja2")

@user_blueprint.route('/news')
@user_decorators.requires_login
def news():
    return render_template("resources.jinja2")