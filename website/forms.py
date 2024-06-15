from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, NumberRange
from flask_wtf.file import FileField, FileRequired


# Forms using flaskforms, not all forms used flaskform

class ShopItemsForm(FlaskForm):
    product_name = StringField('Name of Product', validators=[DataRequired()])
    product_price = FloatField('Price', validators=[DataRequired()])
    in_stock = IntegerField('In Stock', validators=[DataRequired(), NumberRange(min=0)])
    product_picture = FileField('Name of Product', validators=[FileRequired()])
    product_calorie = IntegerField('Calorie', validators=[DataRequired(), NumberRange(min=0)])

    add_product = SubmitField('Add Product')
    update_product = SubmitField('update')

class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('New Password' ,validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('New Password', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Change Password')

class UpdateProfile(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0)])
    height = IntegerField('Height', validators=[DataRequired(), NumberRange(min=0)])
    weight = IntegerField('Weight', validators=[DataRequired(), NumberRange(min=0)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'),], validators=[DataRequired()])
    activity_level = SelectField('Activity Level', choices=[
        ('Sedentary', 'Sedentary'),
        ('Lightly Active', 'Lightly Active'),
        ('Moderately Active', 'Moderately Active'),
        ('Very Active', 'Very Active')
    ], validators=[DataRequired()])
    update_profile = SubmitField('Update')
   


        
    
    
