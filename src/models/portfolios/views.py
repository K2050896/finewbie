import base64
import uuid

import pygal
from pygal.style import DefaultStyle
from flask import Blueprint, request, render_template, session, redirect, url_for
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvas
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

    if request.method == "POST":
        port_opt(cnst, portfolio_id)
        tempPortfolio = Portfolio.from_mongo(portfolio_id)
        return render_template("portfolios/port_details.jinja2", portfolio=tempPortfolio)
    else:
        tempPortfolio = Portfolio.from_mongo(portfolio_id)
        # fig = Portfolio.plot_portfolio(tempPortfolio)
        # canvas = FigureCanvas(fig)
        # img = BytesIO()
        # fig.savefig(img)
        # img.seek(0)
        # plot_data = base64.b64encode(img.read()).decode()
        # return render_template("portfolios/port_details.jinja2", portfolio=tempPortfolio, plot_url=plot_data)
        chart = pygal.Pie(print_values=True, style=DefaultStyle(value_font_size=12,value_colors=('white')))
        chart.title = 'Portfolio Allocation'
        #chart.add(['SPY', 'IWM', 'VEU', 'CSJ', 'BLV', 'Cash Inv'], tempPortfolio['alloc_percent'][-1][0:5])
        chart.add('SPY', tempPortfolio['alloc_percent'][-1][0])
        chart.add('IWM', tempPortfolio['alloc_percent'][-1][1])
        chart.add('VEU', tempPortfolio['alloc_percent'][-1][2])
        chart.add('CSJ', tempPortfolio['alloc_percent'][-1][3])
        chart.add('BLV', tempPortfolio['alloc_percent'][-1][4])
        chart.add('Cash', tempPortfolio['alloc_percent'][-1][5])
        chart.value_formatter = lambda x: "%.2f" % x
        chart = chart.render_data_uri()

        return render_template("portfolios/port_details.jinja2", portfolio=tempPortfolio, chart=chart)