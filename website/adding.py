import base64
from flask import Blueprint, redirect, url_for, render_template, request, session, flash
from sqlalchemy import exc, func
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import db
from . import STORAGE
from .models import Product
from .models import Appliance
from flask_login import login_user, logout_user, login_required, current_user

adding = Blueprint("adding", __name__)

@adding.route("/addProduct", methods=['GET','POST'])
@login_required
def addProduct():
    if request.method == "POST":
        total_product_amount = db.session.query(func.sum(Product.amount)).scalar()
        if total_product_amount is None:
            total_product_amount = 0
        image = request.files['image']
        amount = request.form.get("amount")
        productName = request.form.get("productName")
        location = request.form.get("location")

        if not image or not amount or not location or not productName:
            flash('You need to enter this data!', category='error')
        elif total_product_amount + int(amount) > STORAGE:
            flash('There is no space in warehouse!', category='error')
        else:
            filename = image.filename
            product = Product(img=image.read(), imgName=filename, productName=productName, amount=amount, location=location)
            try:
                db.session.add(product)
                db.session.commit()
                flash('Product added!')
                return redirect(url_for('views.home'))
            except exc.IntegrityError:
                db.session.rollback()
                flash('Unexpected error with Data Base - Try different image!', category='error')

    return render_template("addProduct.html")

@adding.route("/viewProducts", methods=['GET'])
@login_required
def viewProducts():
    products = Product.query.all()
    image_list = []
    for img in products:
        image = base64.b64encode(img.img).decode('ascii')
        image_list.append(image)
    return render_template("viewProducts.html", products=products, image_list=image_list)


@adding.route("/addAppliance", methods=['GET','POST'])
@login_required
def addAppliance():
    if request.method == "POST":
        image = request.files['image']
        applianceName = request.form.get("applianceName")
        condition = request.form.get("condition")

        if not image or not applianceName or not condition:
            flash('You need to enter this data!', category='error')
        else:
            filename = image.filename
            appliance = Appliance(img=image.read(), imgName=filename, applianceName=applianceName, condition=condition)
            try:
                db.session.add(appliance)
                db.session.commit()
                flash('Appliance added!')
                return redirect(url_for('views.home'))
            except exc.IntegrityError:
                db.session.rollback()
                flash('Unexpected error with Data Base - Try different image!', category='error')

    return render_template("addApliance.html")


@adding.route("/deleteProduct/<int:productID>", methods=['POST'])
@login_required
def deleteProduct(productID):
    product = Product.query.get_or_404(productID)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('adding.viewProducts'))


@adding.route("/editProduct_<int:productID>", methods=['GET','POST'])
@login_required
def editProduct(productID):
    total_product_amount = db.session.query(func.sum(Product.amount)).scalar()
    if total_product_amount is None:
        total_product_amount = 0
    product = Product.query.get_or_404(productID)
    img = product.img
    imgName = product.imgName
    productName = product.productName
    amount = product.amount
    location = product.location

    if request.method == "POST":
        new_image = request.files['image']
        new_amount = request.form.get("amount")
        new_productName = request.form.get("productName")
        new_location = request.form.get("location")
        if not new_amount or not new_location or not new_productName:
            flash('You need to enter this data!', category='error')
        elif int(new_amount) != int(amount) and total_product_amount + int(new_amount) > STORAGE:
            flash('There is no space in warehouse!', category='error')
        else:
            if not new_image:
                product.img = img
                product.imgName = imgName
            else:
                new_filename = new_image.filename
                product.img = new_image.read()
                product.imgName = new_filename
            product.productName = new_productName
            product.amount = new_amount
            product.location = new_location
            db.session.commit()
            return redirect(url_for('adding.viewProducts'))

    return render_template("editProduct.html", productName=productName, amount=amount, location=location)


@adding.route("/viewAppliances", methods=['GET'])
@login_required
def viewAppliances():
    appliances = Appliance.query.all()
    image_list = []
    for img in appliances:
        image = base64.b64encode(img.img).decode('ascii')
        image_list.append(image)
    return render_template("viewAppliances.html", appliances=appliances, image_list=image_list)


@adding.route("/deleteAppliance/<int:applianceID>", methods=['POST'])
@login_required
def deleteAppliance(applianceID):
    appliance = Appliance.query.get_or_404(applianceID)
    db.session.delete(appliance)
    db.session.commit()
    return redirect(url_for('adding.viewAppliances'))


@adding.route("/editAppliance_<int:applianceID>", methods=['GET','POST'])
@login_required
def editAppliance(applianceID):
    appliance = Appliance.query.get_or_404(applianceID)
    img = appliance.img
    imgName = appliance.imgName
    applianceName = appliance.applianceName
    condition = appliance.condition

    if request.method == "POST":
        new_image = request.files['image']
        new_condition = request.form.get("condition")
        new_applianceName = request.form.get("applianceName")
        if not new_condition or not new_applianceName:
            flash('You need to enter this data!', category='error')
        else:
            if not new_image:
                appliance.img = img
                appliance.imgName = imgName
            else:
                new_filename = new_image.filename
                appliance.img = new_image.read()
                appliance.imgName = new_filename
            appliance.applianceName = new_applianceName
            appliance.condition = new_condition
            db.session.commit()
            return redirect(url_for('adding.viewAppliances'))

    return render_template("editAppliance.html", applianceName=applianceName, condition=condition)