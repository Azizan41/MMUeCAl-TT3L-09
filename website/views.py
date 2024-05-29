from flask import Blueprint, Flask, request, render_template, redirect, url_for
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

# @views.route('/caloriecounter' , method = ['POST'])
# @login_required
# def calorie_counter():
#     weight = request.form.get('weight')
#     height = request.form.get('height')
#     age = request.form.get('age')
#     gender = request.form.get('gender')
#     activity = request.form.get('activity')

#     daily_calories = calculate_daily_calories(weight, height, age, gender, activity)

#     return render_template('result.html', daily_calories=daily_calories)


@views.route('/caloriecounter')
@login_required
def calorie_counter():
    return render_template("caloriecounter.html")

@views.route('/stepcounter')
@login_required
def step_counter():
    return render_template("stepcounter.html")

@views.route('/exercise')
def exercise():
    # exercises = [
    #     {'name': 'Squats', 'description': 'A lower body exercise'},
    #     {'name': 'Push-ups', 'description': 'An upper body exercise'},
    #     {'name': 'Sit-ups', 'description': 'A core exercise'},
    # ]
    return render_template('exercise.html')





