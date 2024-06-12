from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, length, NumberRange
from flask_wtf.file import FileField, FileRequired

class ShopItemsForm(FlaskForm):
    product_name = StringField('Name of Product', validators=[DataRequired()])
    product_price = FloatField('Price', validators=[DataRequired()])
    in_stock = IntegerField('In Stock', validators=[DataRequired(), NumberRange(min=0)])
    product_picture = FileField('Name of Product', validators=[FileRequired()])

    add_product = SubmitField('Add Product')
    update_product = SubmitField('update')

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('New Password' ,validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('New Password', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Change Password')
    