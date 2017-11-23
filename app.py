# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session
from models.users import User
from models.asset import Asset
from models.portfolio import Portfolio
from common.database import Database



# create the application object
app = Flask(__name__)
app.secret_key = "secret"

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/')
def home():
    return render_template("intro.jinja2")

@app.route('/login')
def login_page():
    return render_template("login.jinja2")

@app.route('/register')
def register_page():
    return render_template("register.jinja2")

@app.route('/auth/register', methods=['POST'])
def register():
    email = request.form["email"]
    password = request.form["password"]

    User.register_user(email, password)
    return render_template("homepage.jinja2", email=session['email'])

@app.route('/auth/login', methods=['POST'])
def login():
    # error = ""
    email = request.form["email"]
    password = request.form["password"]

    if User.login_valid(email, password):
        User.login(email)
    else:
        session["email"] = None

    # if User.get_by_email(email) is None:
    #     error = "No account found. Please sign up!"
    #     return redirect(url_for(signup), email=session["email"])
    # else:
    #     if User.login_valid(email, password):
    #         User.login(email, password)
    #         return redirect(url_for(home), email=session["email"])
    #     else:
    #         error = "Incorrect password! Log in again"
    #         return redirect(url_for(login), email=session["email"])

    return render_template("homepage.jinja2", email=session['email'])

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)