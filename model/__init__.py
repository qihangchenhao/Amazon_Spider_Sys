# config=utf-8
from flask_login import LoginManager

login_manager = LoginManager()

login_manager.login_view = "user.login"
