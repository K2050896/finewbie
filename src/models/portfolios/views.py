import base64
import uuid
from bokeh import embed
import pandas as pd
from flask import Blueprint, request, render_template, session, redirect, url_for
from io import BytesIO
from src.models.users.user import User
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators
from src.models.profiles.profile import Profile
from src.models.portfolios.portfolio import Portfolio
import src.models.portfolios.constants as cnst
from src.models.portfolios.port_opt import port_opt
from bokeh.plotting import figure, output_file, show
from bokeh.charts import Donut, Line

portfolio_blueprint = Blueprint('portfolios', __name__)

@portfolio_blueprint.route('/port-summary/<string:portfolio_id>')
@user_decorators.requires_login
# Gets unique summary of portfolio page - and user can click optimize
def port_summary(portfolio_id):
    temp = Profile.from_mongo(portfolio_id)
    return render_template("portfolios/port_summary.jinja2", profile=temp)

@portfolio_blueprint.route('/optimize/<string:portfolio_id>', methods=['POST'])
@user_decorators.requires_login
def optimize(portfolio_id):
    pie_plot, line_plot, bar_plot = port_opt(cnst, portfolio_id)
    try:
        if pie_plot is not None:
            tempPortfolio = Portfolio.from_mongo(portfolio_id)

            script1, div1 = embed.components(pie_plot)
            script2, div2 = embed.components(line_plot)
            script3, div3 = embed.components(bar_plot)

            return render_template("portfolios/port_details.jinja2", portfolio=tempPortfolio, script1=script1,
                                   div1=div1, script2=script2, div2=div2, script3=script3, div3=div3)

    except TypeError:
        return ("There is no further optimization needed.")
