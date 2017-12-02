import base64
import uuid

import pygal
from bokeh import embed
from pygal.style import DefaultStyle
import pandas as pd
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
from bokeh.plotting import figure, output_file, show
from bokeh.charts import Donut

portfolio_blueprint = Blueprint('portfolios', __name__)

def plot_alloc(port):
    # data = pd.Series(port['alloc_percent'], index=cnst.TICKERS + ['Cash'])
    # pie_chart = Donut(data)
    # return pie_chart
    pass

def plot_reached_dollar(port):
    y = port['reached_dollar']
    time_step = port_opt(cnst, port['port_id'])
    x = [i * time_step for i in range(len(y))]

    plot_line = figure(title="Goal amount reached", x_axis_label='Time', y_axis_label='Value of portfolio')
    plot_line.line(x, y)
    return plot_line

def plot_cont(port):
    # prof = Profile.from_mongo(port['port_id'])
    # y = port['cont']
    # x = range(6)
    #
    # plot_bar = figure(title="Additional contribution from investor", x_axis_label='Time', y_axis_label='Contribution')
    # plot_bar.bar(x, y)
    # return plot_bar
    pass

@portfolio_blueprint.route('/port-summary/<string:portfolio_id>')
@user_decorators.requires_login
# Gets unique summary of portfolio page - and user can click optimize
def port_summary(portfolio_id):
    temp = Profile.from_mongo(portfolio_id)
    return render_template("portfolios/port_summary.jinja2", profile=temp)

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
        # chart = pygal.Pie(print_values=True, style=DefaultStyle(value_font_size=12,value_colors=('white')))
        # chart.title = 'Portfolio Allocation'
        # #chart.add(['SPY', 'IWM', 'VEU', 'CSJ', 'BLV', 'Cash Inv'], tempPortfolio['alloc_percent'][-1][0:5])
        # chart.add('SPY', tempPortfolio['alloc_percent'][-1][0])
        # chart.add('IWM', tempPortfolio['alloc_percent'][-1][1])
        # chart.add('VEU', tempPortfolio['alloc_percent'][-1][2])
        # chart.add('CSJ', tempPortfolio['alloc_percent'][-1][3])
        # chart.add('BLV', tempPortfolio['alloc_percent'][-1][4])
        # chart.add('Cash', tempPortfolio['alloc_percent'][-1][5])
        # chart.value_formatter = lambda x: "%.2f" % x
        # chart = chart.render_data_uri()

        plot_line = plot_reached_dollar(tempPortfolio)
        script, div = embed.components(plot_line)

        return render_template("portfolios/port_details.jinja2", portfolio=tempPortfolio, script=script, div=div)



