import uuid
from flask import Blueprint, request, render_template, session, redirect, url_for
from src.models.users.user import User
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators
from src.models.profiles.profile import Profile
from src.models.portfolios.portfolio import Portfolio
import src.models.portfolios.constants as cnst
from src.models.portfolios.port_opt import port_opt

portfolio_blueprint = Blueprint('portfolios', __name__)


@portfolio_blueprint.route('/port_summary/<string:portfolio_id>')



@portfolio_blueprint.route('/optimize', methods=['POST'])
def optimize():
    profile = Profile.from_mongo('port_id')
    print(profile)
    print("===============")
    portfolio = Portfolio.from_mongo('port_id')
    print(portfolio)
    port_opt(cnst, portfolio, profile)
    print("Optimization in progress................")
    print("HELLOOOOOOO")
    return render_template("portfolios/port_details.jinja2")