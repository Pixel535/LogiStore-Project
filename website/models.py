from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    workerCardID = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(150))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.LargeBinary)
    imgName = db.Column(db.Text)
    productName = db.Column(db.String(150))
    amount = db.Column(db.Integer)
    location = db.Column(db.String(150))

class Appliance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.LargeBinary)
    imgName = db.Column(db.Text)
    applianceName = db.Column(db.String(150))
    condition = db.Column(db.Integer)
