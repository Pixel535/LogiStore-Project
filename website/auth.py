from flask import Blueprint, redirect, url_for, render_template, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user

Auth = Blueprint("auth", __name__)

@Auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if request.form['submit_button'] == 'Register':
            return redirect(url_for('auth.register'))
        elif request.form['submit_button'] == 'Log in':
            workerCardID = request.form.get("workerCardID")
            password = request.form.get("password")

            user = User.query.filter_by(workerCardID=workerCardID).first()
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Password is incorect!', category='error')
            else:
                flash('Worker Card ID does not exists!', category='error')

    return render_template("login.html")


@Auth.route("/logOut")
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@Auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        if request.form['submit_button'] == 'Cancel':
            return redirect(url_for('views.home'))
        elif request.form['submit_button'] == 'Sign up':
            workerCardID = request.form.get("workerCardID")
            username = request.form.get("username")
            password = request.form.get("password")
            role = request.form.get("role")

            workerID_exists = User.query.filter_by(workerCardID=workerCardID).first()
            username_exists = User.query.filter_by(username=username).first()
            if (not workerCardID) or (not username) or (not password) or (not role):
                flash('You need to type something!', category='error')
            elif workerID_exists:
                flash('Worker Card ID already exists!', category='error')
            elif username_exists:
                flash('Username is already in use!', category='error')
            else:
                new_user = User(workerCardID=workerCardID, username=username, role=role, password=generate_password_hash(
                    password, method='scrypt'))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('User created!')
                return redirect(url_for('views.home'))

    return render_template("register.html")

@Auth.route("/registerCancel")
def registerCancel():
    return redirect(url_for('views.home'))


@Auth.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == "POST":
        new_username = request.form.get("username")
        new_password = request.form.get("password")

        if new_username != current_user.username and not new_password:
            username_exists = User.query.filter_by(username=new_username).first()

            if username_exists:
                flash('Username is already in use!', category='error')
            else:
                current_user.username = new_username
                current_user.password = current_user.password
                db.session.commit()
                flash('You changed your profile!')
                return redirect(url_for('views.home'))
        elif new_username != current_user.username and new_password:
            username_exists = User.query.filter_by(username=new_username).first()

            if username_exists:
                flash('Username is already in use!', category='error')
            else:
                current_user.username = new_username
                current_user.password = generate_password_hash(new_password, method='scrypt')
                db.session.commit()
                flash('You changed your profile!')
                return redirect(url_for('views.home'))
        elif new_username == current_user.username and not new_password:
            current_user.username = new_username
            current_user.password = current_user.password
            db.session.commit()
            return redirect(url_for('views.home'))
        elif new_username == current_user.username and new_password:
            current_user.username = new_username
            current_user.password = generate_password_hash(new_password, method='scrypt')
            db.session.commit()
            flash('You changed your profile!')
            return redirect(url_for('views.home'))


    return render_template("profile.html", workerCardID=current_user.workerCardID, username=current_user.username, role=current_user.role)

