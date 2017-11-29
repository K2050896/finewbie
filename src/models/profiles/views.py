from flask import Blueprint, request, render_template, session, redirect, url_for
from src.models.profiles.profile import Profile

profile_blueprint = Blueprint('profiles', __name__)

@profile_blueprint.route('/create-goal', methods=['GET', 'POST'])
def create_goal():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]

    return render_template("profiles/create_goal.jinja2")

@profile_blueprint.route('/risk-profile', methods=['GET', 'POST'])
def risk_profile():
    pass

@profile_blueprint.route('/edit-goal')
def edit_goal():
    pass

