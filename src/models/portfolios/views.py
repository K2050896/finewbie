import uuid
from flask import Blueprint, request, render_template, session, redirect, url_for
from src.models.profiles.profile import Profile
from src.models.portfolios.portfolio import Portfolio
import src.models.portfolios.constants as cnst
from src.models.portfolios.port_opt import port_opt

portfolio_blueprint = Blueprint('portfolios', __name__)

@portfolio_blueprint.route('/optimize')
def optimize():
    profile = Profile.from_mongo(session['port_id'])
    portfolio = Portfolio.from_mongo(session['port_id'])
    port_opt(cnst, portfolio, profile)
    print("Optimization in progress................")
    print("HELLOOOOooOOOOO")
    return render_template("portfolios/port_details.jinja2")