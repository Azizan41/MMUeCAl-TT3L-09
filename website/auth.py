from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import PasswordChangeForm

auth = Blueprint('auth', __name__)





@auth.route('/userauth', methods=['POST', 'GET'])

def userauth():

    if request.method == 'GET':
        return render_template ('logsign.html')
    elif request.method == 'POST':
        action = request.form.get('action')

        if action == 'signup':
            student_id = request.form.get("student_id")
            username = request.form.get('username')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
        
            ID_exists = User.query.filter_by(student_id=student_id).first()
            username_exist = User.query.filter_by(username=username).first()
            if ID_exists or username_exist :
                flash('ID or username already exists.', category='error')
            elif len(student_id) < 10:
                flash('ID must be more than 10 numbers', category='error')
            elif len(password1) < 4:
                 flash('Password must be greater than 3 char', category ='error')
            elif password1 != password2:
                flash('Password doesnt match', category ='error')
            else:
                new_user = User(student_id=student_id, username=username, password = generate_password_hash(password1, method='pbkdf2:sha256'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True) 
                flash('Account Created', category ='success')
                return redirect(url_for('views.home'))
        
        elif action == 'signin':
            print("here")
            student_id = request.form.get("student_id")
            password = request.form.get('password')
 
            user = User.query.filter_by(student_id=student_id).first()
            if user:
                if check_password_hash(user.password, password):
                   flash('Logged In', category='success')
                   login_user(user, remember=True)
                   return redirect(url_for('views.home'))
                else:
                   flash('Password is incorrect', category='error')
            else:
                flash('ID does not exist', category='error')
    return render_template("logsign.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.guest_home"))

@auth.route('/change-password/<int:user_id>', methods=['GET','POST'])
@login_required
def change_password(user_id):
    form = PasswordChangeForm()
    return render_template("changepassword.html", form=form)