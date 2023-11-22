from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

Views = Blueprint("views", __name__)

@Views.route("/")
@Views.route("/home")
@login_required
def home():
    return render_template("home.html", username=current_user.username)


@Views.route("/viewItems")
@login_required
def viewItems():
    return render_template("viewItems.html")


@Views.route("/addItems")
@login_required
def addItems():
    return render_template("addItems.html")


@Views.route("/raportChoice")
@login_required
def raportChoice():
    if current_user.role == 'Admin':
        return render_template("raportChoice.html")
    else:
        flash('You need to be an Admin to access this page!', category='error')
        return redirect(url_for('views.home'))
