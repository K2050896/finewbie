import uuid
from flask import Blueprint, request, render_template, session, redirect, url_for
from src.models.profiles.profile import Profile
from src.models.portfolios.portfolio import Portfolio
import src.models.portfolios.port_opt

portfolio_blueprint = Blueprint('portfolios', __name__)

@portfolio_blueprint.route('/optimize')
def optimize():
    #portfolio = Portfolio()
    pass
