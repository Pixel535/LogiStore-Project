from io import BytesIO
import plotly.graph_objects as go
import pandas as pd
from flask import Blueprint, redirect, url_for, render_template, request, session, flash
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import STORAGE
from .models import User
from .models import Product
from .models import Appliance
from flask_login import login_user, logout_user, login_required, current_user
import plotly.express as px

admin = Blueprint("admin", __name__)

@admin.route("/seeUsers", methods=['GET'])
@login_required
def seeUsers():
    if current_user.role == 'Admin':
        users = User.query.all()
        return render_template('seeUsers.html', users=users)
    else:
        flash('You need to be an Admin to access this page!', category='error')
        return redirect(url_for('views.home'))


@admin.route("/deleteUser/<int:userID>", methods=['POST'])
@login_required
def deleteUser(userID):
    if current_user.role == 'Admin':
        user = User.query.get_or_404(userID)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('admin.seeUsers'))
    else:
        flash('You need to be an Admin to access this page!', category='error')
        return redirect(url_for('views.home'))


@admin.route("/warehouseCheck", methods=['GET'])
@login_required
def warehouseCheck():
    if current_user.role == 'Admin':
        #GRAPH 1
        total_product_amount = db.session.query(func.sum(Product.amount)).scalar()
        data = pd.DataFrame({'Category': ['Used Space', 'Available Space'],
                             'Value': [total_product_amount, STORAGE - total_product_amount]})
        fig = px.pie(data, names='Category', values='Value', title='Warehouse Space Utilization')
        plot_1 = fig.to_html(full_html=False)

        # GRAPH 2
        avg_condition = db.session.query(func.avg(Appliance.condition)).scalar() or 0
        fig = go.Figure()

        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=avg_condition,
            title='Average Machine Condition',
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [None, 100]},
                   'steps': [{'range': [0, 100], 'color': "#00FF00"}],
                   'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': avg_condition}},
            number={'suffix': "%"}
        ))
        plot_2 = fig.to_html(full_html=False)

        # GRAPH 3
        appliances = Appliance.query.all()
        machine_names = [machine.applianceName for machine in appliances]
        condition_values = [machine.condition for machine in appliances]
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=machine_names,
            y=condition_values,
            marker_color='blue',
            text=condition_values,
            textposition='outside',
            hoverinfo='y+text',
        ))

        fig.update_layout(
            title='Machine Condition State',
            xaxis=dict(title='Machine Name'),
            yaxis=dict(title='Consumption (%)'),
            barmode='group',
        )

        plot_3 = fig.to_html(full_html=False)

        # GRAPH 4
        products = Product.query.all()
        product_amounts = [product.amount for product in products]
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=product_amounts,
            y=condition_values,
            mode='markers',
            marker=dict(color='red', size=10),
            text=[f'Product: {amount}, Machine Condition: {consumption}' for amount, consumption in
                  zip(product_amounts, condition_values)],
            hoverinfo='text'
        ))

        fig.update_layout(
            title='Correlation Between Product Amount and Machine Condition',
            xaxis=dict(title='Product Amount'),
            yaxis=dict(title='Machine Consumption (%)'),
        )

        plot_4 = fig.to_html(full_html=False)

        # GRAPH 5
        locations = list(set([product.location for product in products]))
        product_counts_by_location = [
            db.session.query(func.sum(Product.amount)).filter(Product.location == location).scalar() or 0 for location
            in locations]
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=locations,
            y=product_counts_by_location,
            marker_color='green',
            text=product_counts_by_location,
            textposition='outside',
            hoverinfo='y+text'
        ))

        fig.update_layout(
            title='Comparison of Product Amounts in Different Locations',
            xaxis=dict(title='Location'),
            yaxis=dict(title='Product Amount'),
        )

        plot_5 = fig.to_html(full_html=False)
        return render_template('warehouseCheck.html', plot_1=plot_1, plot_2=plot_2, plot_3=plot_3, plot_4=plot_4, plot_5=plot_5)
    else:
        flash('You need to be an Admin to access this page!', category='error')
        return redirect(url_for('views.home'))