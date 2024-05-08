from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "users_info.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY'] = 'ayamgoreng'
    app.secret_key = 'ayamgoreng'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')


    from .views import views
    from .auth import auth
    from .admin import admin
    from .models import User, Cart, Product, Order

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(admin, url_prefix = '/')
    

    from .models import User, Weight

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

  

    return app
