import uuid
from flask import Blueprint, request, render_template, session, redirect, url_for, flash
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
        goal = float(request.form["amount"])
        horizon = float(request.form["time"])
        time_left = float(request.form["time"])
        importance = request.form["imp"]
        init_con = request.form["init_con"]
        assets = float(request.form["assets"])
        liab = float(request.form["liab"])
        r1 = request.form["r1"]
        r2 = request.form["r2"]
        r3 = request.form["r3"]
        r4 = request.form["r4"]
        r5 = request.form["r5"]

        profile = Profile(port_id=port_id, user_email=user_email, name=name, goal=goal, horizon=[horizon], time_left=time_left, importance=importance, init_con=init_con,
                          dis_inc=[assets-liab], r1=r1, r2=r2, r3=r3, r4=r4, r5=r5)
        profile.save_to_mongo()
        flash("Congrats! You just created a new goal for yourself!")
        return redirect(url_for('portfolios.port_summary', portfolio_id=session['curr_port']))

    return render_template("profiles/create_goal.jinja2")


@profile_blueprint.route('/my-goals')
@user_decorators.requires_login
def my_goals():
    port_ids = User.get_port_ids(session['email'])
    portfolios = []
    for i in port_ids:
        portfolios.append(Portfolio.from_mongo(i))
    return render_template("profiles/my_goals.jinja2", portfolios=portfolios)


@profile_blueprint.route('/edit-goal/<string:portfolio_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_goal(portfolio_id):
    temp = Profile.from_mongo(portfolio_id)
    old_time_left = float(temp['time_left'])
    old_horizon = float(temp['horizon'][-1])
    if request.method == "POST":
        goal = float(request.form["amount"])
        horizon = float(request.form["time"])
        assets = float(request.form["assets"])
        liab = float(request.form["liab"])
        temp["horizon"].append(horizon)
        temp["dis_inc"].append(assets-liab)
        Profile.update_profile(temp['port_id'],
                               {"port_id": temp['port_id'], "user_email": temp['user_email'], "name": temp['name'],
                                "goal": goal, "horizon": temp['horizon'],
                                "time_left": old_time_left + horizon - old_horizon,
                                "init_con": temp['init_con'], "dis_inc": temp['dis_inc'], "init_alloc": temp['init_alloc'],
                                "lamb": temp['lamb'], "importance": temp['importance']})
        temp = Profile.from_mongo(portfolio_id)
        flash("Successfully Edited Goal!")
        return redirect(url_for('portfolios.port_summary', portfolio_id=portfolio_id, profile=temp))
    return render_template("profiles/edit_goal.jinja2", portfolio_id=portfolio_id, profile=temp)