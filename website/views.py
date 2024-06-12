from flask import Blueprint, render_template, request, flash, redirect, request, jsonify, url_for
from flask_login import login_required, current_user
from .models import User, Product, Cart, Order, Routes, Activity
from . import db
import sqlite3
from sqlalchemy import desc
from collections import defaultdict
from datetime import datetime
from .forms import UpdateProfile

views = Blueprint('views', __name__)


db_path = 'instance/users_info.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS routes
             (id INTEGER PRIMARY KEY, start_point TEXT, end_point TEXT, calories REAL, steps INTEGER)''')
conn.commit()
conn.close()

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

@views.route('/update-profile/<int:user_id>', methods={'GET', 'POST'})
@login_required
def update_profile(user_id):
     user = User.query.get(user_id)
     user_to_update = User.query.get(user_id)
     
     if current_user.id == user_id:
        form = UpdateProfile(obj=user_to_update)
        form.student_id.render_kw ={'placeholder': user.id}
        form.username.render_kw ={'placeholder': user.username}
        form.age.render_kw ={'placeholder': user.age}
        form.height.render_kw ={'placeholder': user.height}
        form.weight.render_kw ={'placeholder': user.weight}
        form.gender.render_kw ={'placeholder': user.gender}
        form.activity_level.render_kw ={'placeholder': user.activity_level}


        if form.validate_on_submit():
         username = form.username.data
         age = form.age.data
         height = form.height.data
         weight = form.weight.data
         gender = form.gender.data
         activity_level = form.activity_level.data

         try:
             User.query.filter_by(id=user_id).update(dict(username=username , 
                                                          age=age , 
                                                          height=height , 
                                                          weight=weight ,
                                                          gender=gender ,
                                                          activity_level=activity_level))
             db.session.commit()
             return redirect (url_for('views.profile'))
         except Exception as e:
             print('Profile Not Updated', e)
        return render_template('profile.html', form=form, user=user)
     return render_template('404.html')
    


@views.route('/caloriecounter')
@login_required
def calorie_counter():

    activity_log = Activity.query.filter_by(customer_link = current_user.id).order_by(desc(Activity.date_added)).all()
    food_log = Order.query.filter_by(customer_link = current_user.id).order_by(desc(Order.date_created)).all()
    
    activity_grouped = defaultdict(list)
    total_calories_consumed = defaultdict(float)
    total_calories_burned = defaultdict(float)

    for activity in activity_log:
        year = activity.date_added.year
        month = activity.date_added.month
        day = activity.date_added.day

        date_obj = datetime(year, month, day)
        date_format = date_obj.strftime("%Y/%m/%d")

        activity_grouped[date_format].append(activity)
        total_calories_burned[date_format] += activity.calorie_burned
    
    
    for order in food_log:
        year = order.date_created.year
        month = order.date_created.month
        day = order.date_created.day

        date_obj = datetime(year, month, day)
        date_format = date_obj.strftime("%Y/%m/%d")

        activity_grouped[date_format].append(order)
        total_calories_consumed[date_format] += order.calories


    routes = Routes.query.all()
    for route in routes:
     return render_template('caloriecounter.html', total_calories_burned = total_calories_burned, activity_grouped=activity_grouped, total_calories_consumed=total_calories_consumed)

@views.route('/stepcounter', methods=['GET', 'POST'])
@login_required
def step_counter():

    db_path = 'instance/users_info.db'

    if request.method == 'POST':
        start_point = request.form['start_point']
        end_point = request.form['end_point']
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT id, calories, steps FROM routes WHERE start_point=? AND end_point=?", (start_point, end_point))
        result = c.fetchone()
        conn.close()
        if result:
            id = result[0]
            calories = result[1]
            steps = result[2]

            return render_template('stepburner.html', id=id, calories=calories, steps=steps, start_point=start_point, end_point=end_point)
        else:
            return render_template('stepburner.html', error="Route not found", start_point=start_point, end_point=end_point)
    return render_template('stepburner.html')


@views.route('/stepcounter/<int:routes_id>')
@login_required
def record_step_counter(routes_id):
    routes_to_record = Routes.query.get(routes_id)

    if routes_to_record:
        try:
            new_activity = Activity(
                customer_link=current_user.id,
                routes_id=routes_id,
                calorie_burned=routes_to_record.calories,
                date_added=datetime.now()
            )

            db.session.add(new_activity)
            db.session.commit()
            flash('Routes added successfully')
            return redirect(request.referrer)
        except Exception as e:
            db.session.rollback()
            flash('Error adding steps')
            print(e)
            return redirect(request.referrer)
    else:
        flash('Route not found')
        return redirect(request.referrer)


@views.route('/cart/<int:product_id>')
@login_required
def cart(product_id):
    product_to_add = Product.query.get(product_id)
    product_name = product_to_add.product_name
    product_exists = Cart.query.filter_by(product_link=product_id, customer_link=current_user.id).first()
    if product_exists:
        try:
            product_exists.quantity = product_exists.quantity + 1
            db.session.commit()
            flash(f' Quantity of { product_exists.product.product_name } has been updated')
            return redirect(request.referrer)
        except Exception as h:
            print('Cart failed to update', h )
            flash(f'Quantity of { product_exists.product.product_name } update failed')
            return redirect(request.referrer)
        

    new_cart_product = Cart(quantity=1, customer_link=current_user.id, product_link=product_id, product_name = product_name)
    new_cart_product.quantity =+ 1
    new_cart_product.product_link = product_to_add.id
    new_cart_product.customer_link = current_user.id

    try:
        db.session.add(new_cart_product)
        db.session.commit()
        flash(f' { new_cart_product.product.product_name } added to cart')
        print('item added')
    except Exception as j:
        print ("Product failed to add to cart",j)
        flash(f'{ new_cart_product.product.product_name } has not been added to cart')

    return redirect(request.referrer)


@views.route('/cart')
@login_required
def show_cart():
    cart_items = Cart.query.filter_by(customer_link=current_user.id).all()
    total_price = 0
    total_calories = 0

    for item in cart_items:
            total_price += item.product.product_price * item.quantity
            total_calories += item.product.product_calorie * item.quantity

    return render_template('cart.html', cart=cart_items, total_calories=total_calories,  total_price=total_price)


@views.route('/pluscart')
@login_required
def plus_cart():
    if request.method == 'GET':
        cart_id = request.args.get('cart_id')
        print(cart_id)

        data = {
            'Response':'Backend Response'
        }

        return jsonify(data)
    

@views.route('/place-order')
@login_required
def place_order():
    customer_cart = Cart.query.filter_by(customer_link = current_user.id).all()
    if customer_cart: 
        try:
            for item in customer_cart:
               
               total_item = item.product.product_price * item.quantity
               product_calories = item.product.product_calorie * item.quantity
               product_name = item.product.product_name

            
               order_history = Order(
                  quantity = item.quantity,
                  price = total_item,
                  calories = product_calories,
                  product_name = product_name,
    
                  product_link = item.product_link,
                  customer_link = item.customer_link,
               )


               product = Product.query.get(item.product_link)
               product.in_stock -= item.quantity

               db.session.delete(item)

               db.session.add(order_history)
               

            db.session.commit()


            flash('Order Placed Successfully')
            return ('Order Placed')
        
        except Exception as e:
            print(e)
            db.session.rollback()
            flash('Order Failed')
            return redirect('/')
    else:
        flash('Your cart is empty')
        return redirect('/')
    

@views.route('/history')
@login_required
def history():

    order_history = Order.query.filter_by(customer_link = current_user.id).order_by(desc(Order.date_created)).all()

    order_grouped = defaultdict(list)
    total_prices = defaultdict(float)
    total_calories = defaultdict(int)

    for order in order_history:
        order_grouped [order.date_created].append(order)
        total_prices[order.date_created] += order.price
        total_calories[order.date_created] += order.calories


    return render_template('order_history.html', order_grouped=order_grouped, total_prices=total_prices, total_calories=total_calories )

@views.route('/activity_log')
@login_required
def activity_log():

    
    activity_log = Activity.query.filter_by(customer_link = current_user.id).order_by(desc(Activity.date_added)).all()
    food_log = Order.query.filter_by(customer_link = current_user.id).order_by(desc(Order.date_created)).all()
    
    activity_grouped = defaultdict(list)
    total_calories_consumed = defaultdict(float)
    total_calories_burned = defaultdict(float)

    for activity in activity_log:
        year = activity.date_added.year
        month = activity.date_added.month
        day = activity.date_added.day

        date_obj = datetime(year, month, day)
        date_format = date_obj.strftime("%Y/%m/%d")

        activity_grouped[date_format].append(activity)
        total_calories_burned[date_format] += activity.calorie_burned
    
    
    for order in food_log:
        year = order.date_created.year
        month = order.date_created.month
        day = order.date_created.day

        date_obj = datetime(year, month, day)
        date_format = date_obj.strftime("%Y/%m/%d")

        activity_grouped[date_format].append(order)
        total_calories_consumed[date_format] += order.calories
        

    return render_template('activitylog.html', total_calories_burned = total_calories_burned, activity_grouped=activity_grouped, total_calories_consumed=total_calories_consumed)



<<<<<<< HEAD
    return render_template('cart.html', cart=cart, amount=amount, total=amount)
=======







>>>>>>> main
