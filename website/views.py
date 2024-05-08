from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import User

views = Blueprint('views', __name__)

@views.route('/')
def guest_home():
    return render_template("guest_home.html")

@views.route('/home')
@login_required
def home():
    return render_template("home.html")

@views.route('/foodorder')
@login_required
def foodorder():
    return render_template("foodorder.html")

@views.route('/profile')
@login_required
def profile():
    user_id = current_user.id
    return render_template('profile.html', user_id=user_id)

@views.route('/caloriecounter')
@login_required
def calorie_counter():
    return render_template("caloriecounter.html")

@views.route('/stepcounter')
@login_required
def step_counter():
    return render_template("stepcounter.html")





