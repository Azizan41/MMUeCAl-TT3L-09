from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)




@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        student_id = request.form.get("student_id")
        password = request.form.get('password')

        user = User.query.filter_by(student_id=student_id).first()
        if user :
            if check_password_hash(user.password, password):
                flash('Logged In', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('ID does not exist', category='error')        
    return render_template("login.html")


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        student_id = request.form.get("student_id")
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        ID_exists = User.query.filter_by(student_id=student_id).first()
        if ID_exists:
            flash('ID already exists.', category='error')
        elif len(student_id) < 10:
            flash('ID must be more than 10 numbers', category='error')
        elif len(password1) < 4:
            flash('Password must be greater than 3 char', category ='error')
        elif password1 != password2:
            flash('Password doesnt match', category ='error')
        else:
            new_user = User(student_id=student_id, password = generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) 
            flash('Account Created', category ='success')
            return redirect(url_for('views.home'))


    return render_template("signup.html")


@auth.route('/change-password')
@login_required
def change_password():
    logout_user()
    return render_template("changepassword.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.guest_home"))
