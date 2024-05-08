from . import db
from flask_login import UserMixin
from sqlalchemy import func
from datetime import datetime

class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Float)
    data = db.Column(db.DateTime(timezone=True), default=func.now())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(50))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    cart_items = db.relationship('Cart', backref=db.backref('uer', lazy=True))
    orders = db.relationship('Order', backref=db.backref('user', lazy=True))



class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), unique=True, nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Integer, nullable=False)
    product_picture = db.Column(db.String(1000), unique=True, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    carts = db.relationship('Cart', backref=db.backref('product', lazy=True))
    orders = db.relationship('Order', backref=db.backref('product', lazy=True))



class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    customer_link = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)



class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    payment_id = db.Column(db.String(1000), nullable=True)

    customer_link = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_link = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)