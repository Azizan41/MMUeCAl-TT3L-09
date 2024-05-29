from flask import Blueprint, render_template, flash, send_from_directory, redirect
from flask_login import login_required, current_user
from .forms import ShopItemsForm
from werkzeug.utils import secure_filename
from .models import Product
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/list_product')
def list_food():
    if current_user.admin == True:
        foods = Product.query.order_by(Product.product_name).all()
        return render_template('listfood.html', foods=foods)
    return render_template('404.html')



@admin.route('/website/static/foods/<path:filename>')
def get_image(filename):
    return send_from_directory('../website/static/foods/',filename)



@admin.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.admin == True:
        form = ShopItemsForm()
        if form.validate_on_submit():
            product_name = form.product_name.data
            product_price = form.product_price.data
            in_stock = form.in_stock.data
            
            file = form.product_picture.data

            file_name = secure_filename(file.filename)

            file_path = f'./website/static/foods/{file_name}'

            file.save(file_path)

            new_item = Product()
            new_item.product_name = product_name
            new_item.product_price = product_price
            new_item.product_name = product_name
            new_item.in_stock = in_stock

            new_item.product_picture = file_path

            try:
                db.session.add(new_item)
                db.session.commit()
                flash(f'{product_name} added ')
                print('Item added')
                return render_template('admin.html')
            except Exception as e:
                print(e)
                flash('Item Not Added')

        return render_template('addfood.html', form=form)
    return render_template('404.html')

@admin.route('/update-product/<int:product_id>', methods={'GET', 'POST'})
@login_required
def update_product(product_id):
    if current_user.admin == True:
        form = ShopItemsForm()

        food_to_update = Product.query.get(product_id)
        
        form.product_name.render_kw ={'placeholder': food_to_update.product_name}
        form.product_price.render_kw ={'placeholder': food_to_update.product_price}
        form.in_stock.render_kw ={'placeholder': food_to_update.in_stock}
        
        if form.validate_on_submit():
            product_name = form.product_name.data
            product_price = form.product_price.data
            in_stock = form.in_stock.data

            file = form.product_picture.data

            file_name = secure_filename(file.filename)
            file_path = f'./website/static/foods/{file_name}'

            file.save(file_path)

            try:
                Product.query.filter_by(id=product_id).update(dict(product_name=product_name , 
                                                                   product_price=product_price , 
                                                                   in_stock=in_stock , 
                                                                   product_picture=file_path))
                db.session.commit()
                flash (f' {product_name} updated successfully')
                print('prodak apdet saksesfuli')
                return redirect('/list_product')
            except Exception as j:
                print('Product update cancelled', j)
                flash('Item Not Updated')

        return render_template('updatefood.html', form=form)
    return render_template('404.html')

@admin.route('/remove-product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def remove_product(product_id):
  if current_user.admin == True:
      try:
        print('hello')
        food_to_remove = Product.query.get(product_id)
        db.session.delete(food_to_remove)
        db.session.commit()
        product_name = Product.product_name
        flash(f'{ product_name } deleted ')
        return redirect('/list_product')
      except Exception as g:
          print('fud dilited')
          flash(product_name + 'not deleted')
      return redirect('/list_product')
  return render_template('404.html')

    