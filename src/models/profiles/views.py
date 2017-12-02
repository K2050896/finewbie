import uuid
from flask import Blueprint, request, render_template, session, redirect, url_for
from src.models.profiles.profile import Profile
from src.models.users.user import User
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators
from src.common.database import Database
from src.models.portfolios.portfolio import Portfolio


profile_blueprint = Blueprint('profiles', __name__)

@profile_blueprint.route('/create-goal', methods=['GET', 'POST'])
@user_decorators.requires_login
def create_goal():
    if request.method == 'POST':
        port_id = uuid.uuid4().hex
        session['curr_port'] = port_id
        user_email = session['email']
        name = request.form["name"]
        goal = request.form["amount"]
        horizon = request.form["time"]
        time_left = request.form["time"]
        importance = request.form["imp"]
        init_con = request.form["init_con"]
        assets = request.form["assets"]
        liab = request.form["liab"]
        r1 = request.form["r1"]
        r2 = request.form["r2"]
        r3 = request.form["r3"]
        r4 = request.form["r4"]
        r5 = request.form["r5"]

        profile = Profile(port_id=port_id, user_email=user_email, name=name, goal=goal, horizon=[float(horizon)], time_left=time_left, importance=importance, init_con=init_con,
                          dis_inc=[float(assets)-float(liab)], r1=r1, r2=r2, r3=r3, r4=r4, r5=r5)
        profile.save_to_mongo()

        return redirect(url_for('portfolios.port_summary', portfolio_id=session['curr_port']))

    return render_template("profiles/create_goal.jinja2")


@profile_blueprint.route('/my-goals')
@user_decorators.requires_login
def my_goals():
    port_ids = User.get_port_ids(session['email'])
    portfolios = []
    for i in port_ids:
        portfolios.append(Portfolio.from_mongo(i))
        print(portfolios)
    return render_template("profiles/my_goals.jinja2", portfolios=portfolios)


@profile_blueprint.route('/edit-goal/<string:portfolio_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_goal(portfolio_id):
    temp = Profile.from_mongo(portfolio_id)
    if request.method == "POST":
        goal = request.form["amount"]
        horizon = request.form["time"]
        assets = request.form["assets"]
        liab = request.form["liab"]
        Profile.update_profile(temp['port_id'],
                               {"port_id": temp['port_id'], "user_email": temp['user_email'], "name": temp['name'],
                                "goal": goal, "horizon": [float(horizon)],
                                "time_left": temp['time_left'],
                                "init_con": temp['init_con'], "dis_inc": [float(assets)-float(liab)], "init_alloc": temp['init_alloc'],
                                "lamb": temp['lamb'], "importance": temp['importance']})
        return render_template("profiles/edit_goal.jinja2", portfolio_id=portfolio_id)
    return render_template("profiles/edit_goal.jinja2", portfolio_id=portfolio_id)