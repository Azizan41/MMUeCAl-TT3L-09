from . import db
from flask_login import UserMixin
from sqlalchemy import func
from datetime import datetime
from werkzeug.security import check_password_hash

class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Float)
    data = db.Column(db.DateTime(timezone=True), default=func.now())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(50))
    weight = db.Column(db.Float)
    height = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    activity_level = db.Column(db.String(20))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    admin = db.Column(db.Boolean)

    cart_items = db.relationship('Cart', backref=db.backref('user', lazy=True))
    orders = db.relationship('Order', backref=db.backref('user', lazy=True))


    def verify_password(self, password):
        return check_password_hash(self.password, password)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), unique=True, nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)
    product_picture = db.Column(db.String(1000), unique=True, nullable=False)
    product_calorie = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    carts = db.relationship('Cart', backref=db.backref('product', lazy=True))
    orders = db.relationship('Order', backref=db.backref('product', lazy=True))



class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(100), unique=True, nullable=False)

    customer_link = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    



class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    

    customer_link = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_link = db.Column(db.String(100), db.ForeignKey('product.id'), nullable=False)

class Venue(db.Model):
    __tablename__ = 'distance'
    id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(100), unique=True, nullable=False)
    venue_steps = db.Column(db.Float, nullable=False)

class Routes(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    start_point = db.Column(db.String(50), unique=True)
    end_point = db.Column(db.String(50), unique=True)
    calories = db.Column(db.Float)
    steps = db.Column(db.Integer)

    activity = db.relationship('Activity', backref=db.backref('routes', lazy=True))

class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True)
    calorie_burned = db.Column(db.Float)
    steps = db.Column(db.Integer)
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())

    routes_id = db.Column(db.Integer, db.ForeignKey('routes.id'))
    customer_link = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


