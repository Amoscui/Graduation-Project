#--coding:utf8--
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, flash
from flask_login import LoginManager
import sys
import importlib
from DB.operate import se
from DB.orm import User
from web.forms import MainForm
from web import webapp as web_blueprint

app = Flask(__name__, static_folder='', static_url_path='')
bootstrap = Bootstrap(app)

# api = restful.Api(app)

app.config['SECRET_KEY'] = 'youcouldneverknowhis-name'

app.config.from_object(__name__)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'web.userLogin'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    return se.session.query(User).filter_by(id=userid).first()


if __name__ == "__main__":
    app.register_blueprint(web_blueprint)
    app.run(debug=True)


