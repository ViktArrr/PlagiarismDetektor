from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config.from_object('config')
db=SQLAlchemy(app)

'''
логин((((((

# from flask_login import LoginManager, current_user
# login_manager=LoginManager()
# login_manager.init_app(app)

# from app.models import User
# login_manager.login_view='User.login'

# @login_manager.user_loader
# def load_user(user_id):
    # return User.query.filter(User.id==int(user_id)).first()

'''

# from flask_cachecontrol import FlaskCacheControl, dont_cache

# flask_cache_control=FlaskCacheControl()
# flask_cache_control.init_app(app)

from app import views, models