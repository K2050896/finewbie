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


@portfolio_blueprint.route('/port-summary/<string:portfolio_id>')
@user_decorators.requires_login
# Gets unique summary of portfolio page - and user can click optimize
def port_summary(portfolio_id):
    temp = Profile.from_mongo(portfolio_id)
    return render_template("portfolios/port_summary.jinja2", portfolio=temp)

@portfolio_blueprint.route('/optimize/<string:portfolio_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def optimize(portfolio_id):
    tempPortfolio = Portfolio.from_mongo(portfolio_id)
    if request.method == "POST":
        port_opt(cnst, portfolio_id)
        return render_template("portfolios/port_details.jinja2", portfolio=tempPortfolio)
    return render_template("portfolios/port_details.jinja2", portfolio=tempPortfolio)