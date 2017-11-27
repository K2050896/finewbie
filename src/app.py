# import the Flask class from the flask module
from flask import Flask, render_template, request, session
from src.common.database import Database
from src.models.users.user import User

# create the application object
app = Flask(__name__)
app.config.from_pyfile('config.py') # app.config.from_object('config') before heroku fix
app.secret_key = "secret"
app.config['SECRET_KEY'] = "secret"

@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/')
def home():
    return render_template("intro.jinja2")

# Import all views
from src.models.users.views import user_blueprint

# Register views in Flask app
app.register_blueprint(user_blueprint, url_prefix = '/users')


@app.route('/login')
def login_page():
    return render_template("users/login.jinja2")

@app.route('/register')
def register_page():
    return render_template("users/register.jinja2")

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
