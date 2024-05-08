from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .forms import ShopItemsForm

admin = Blueprint('admin', __name__)

@admin.route('/admin', methods=['GET', 'POST'])
@login_required
def add_food():
    if current_user.id == 1:
        form = ShopItemsForm()
        return render_template('admin.html', form=form)
    return render_template('404.html')