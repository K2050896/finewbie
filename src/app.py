# import the Flask class from the flask module
from flask import Flask, render_template, request, session
from src.common.database import Database
from src.models.users.user import User

# create the application object
app = Flask(__name__)
app.config.from_pyfile('config.py') # app.config.from_object('config') before heroku fix
app.secret_key = "secret"
#app.config['SECRET_KEY'] = "secret"
#app.config['SESSION_TYPE'] = 'filesystem'


@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/')
def home():
    return render_template("intro.jinja2")

# Import all views
from src.models.users.views import user_blueprint
from src.models.profiles.views import profile_blueprint
from src.models.portfolios.views import portfolio_blueprint

# Register views in Flask app
app.register_blueprint(user_blueprint, url_prefix = '/users')
app.register_blueprint(profile_blueprint, url_prefix = '/profiles')
app.register_blueprint(portfolio_blueprint, url_prefix = '/portfolios')
