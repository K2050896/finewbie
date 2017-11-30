import uuid
from flask import Blueprint, request, render_template, session, redirect, url_for
from src.models.profiles.profile import Profile

profile_blueprint = Blueprint('profiles', __name__)

@profile_blueprint.route('/create-goal', methods=['GET', 'POST'])
def create_goal():
    if request.method == 'POST':
        port_id = uuid.uuid4().hex
        session['curr_port'] = port_id
        user_email = session['email']
        name = request.form["name"]
        goal = request.form["amount"]
        Y = request.form["time"]
        T = request.form["time"]
        importance = request.form["imp"]
        init_con = request.form["init_con"]
        assets = request.form["assets"]
        liab = request.form["liab"]
        r1 = request.form["r1"]
        r2 = request.form["r2"]
        r3 = request.form["r3"]
        r4 = request.form["r4"]
        r5 = request.form["r5"]

        profile = Profile(port_id=port_id, user_email=user_email, name=name, goal=goal, Y=Y, T=T, importance=importance, init_con=init_con,
                          dis_inc=float(assets)-float(liab), r1=r1, r2=r2, r3=r3, r4=r4, r5=r5)
        profile.save_to_mongo()

        print("It got here!")
        return render_template("portfolios/port_summary.jinja2", port_id=session['curr_port'], user_email=session['email'])

    return render_template("profiles/create_goal.jinja2")

# @profile_blueprint.route('/port-summary')
# def port_summary():
#     print("This is the new portfolio.")
#     return render_template("portfolios/port_summary.jinja2", user_email=session['email'])

@profile_blueprint.route('/edit-goal')
def edit_goal():
    pass

@profile_blueprint.route('/my-goals')
def my_goals():
    pass

@profile_blueprint.route('')
