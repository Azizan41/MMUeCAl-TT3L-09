from flask import Blueprint, render_template, request, flash, redirect, request
from flask_login import login_required, current_user
from .models import User, Product, Cart
from . import db

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
    foods = Product.query.order_by(Product.date_added).all()
    return render_template("foodorder.html", foods=foods, cart=Cart.query.filter_by(customer_link=current_user.id).all()
                           if current_user.is_authenticated else [])

@views.route('/profile')
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template('profile.html', user=user)

@views.route('/caloriecounter')
@login_required
def calorie_counter():
    return render_template("caloriecounter.html")

@views.route('/stepcounter')
@login_required
def step_counter():
    return render_template("stepcounter.html")

@views.route('/exercise')
@login_required
def exercise():
    return render_template("exercise.html")

@views.route('/cart/<string:product_name>')
@login_required
def cart(product_name):
    product_to_add = Product.query.get(product_name)
    product_exists = Cart.query.filter_by(product_link=product_name, customer_link=current_user.id).first()
    if product_exists:
        try:
            product_exists.quantity = product_exists.quantity + 1
            db.session.commit()
            return redirect(request.referrer)
        except Exception as h:
            print('Cart failed to update', h )
            flash(f'Quantity of { product_exists.product.product_name } update failed')
            return redirect(request.referrer)
        

    new_cart_product = Cart(quantity=1, customer_link=current_user.id, product_link=product_name)
    new_cart_product.quantity =+ 1
    new_cart_product_link = product_to_add.id
    new_cart_customer_link = current_user.id

    try:
        db.session.add(new_cart_product)
        db.session.commit()
        flash(f' { product_to_add.product_name } added to cart')
        print('item added')
    except Exception as j:
        print ("Product failed to add to cart",j)
        flash(f'{ product_to_add.product_name } has not been added to cart')

    return redirect(request.referrer)


@views.route('/cart')
@login_required
def show_cart():
    cart_items = Cart.query.filter_by(customer_link=current_user.id).all()
    amount = 0
    for product in cart:
        amount += product.product.product_price * product.quantity

    return render_template('cart.html', cart=cart, amount=amount, total=amount)







