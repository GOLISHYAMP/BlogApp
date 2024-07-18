import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS
from itsdangerous import URLSafeSerializer as Serializer
from flask_mail import Mail
from flaskblog.config import Config

app = Flask(__name__)
app.config.from_object(Config)
# secret key can be created by :
# import secrets
# secrets.token_hex(20)
# app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# important while changing the database
# Only this thing need to be changed while changing database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# creating the instance of the database
# db = SQLAlchemy(app)
# For encrpting the password fields
# bcrypt = Bcrypt(app)
# For managing the login related things
# login_manager = LoginManager(app)
# to enable CROSS ORIGIN RESOURCE SHARING
# CORS(app)
# if access unauthorized page then redirect to login page
# login_manager.login_view = 'users.login' # it is a function name of route
# To set the category of the message if raise by the login manager
# login_manager.login_message_category = 'info'

# setting for the mail sending functionality
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('DEMO_EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('DEMO_EMAIL_PASS')
# mail = Mail(app)
# from flaskblog.users.routes import users
# from flaskblog.posts.routes import posts
# from flaskblog.main.routes import main

# app.register_blueprint(users)
# app.register_blueprint(posts)
# app.register_blueprint(main)

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' # it is a function name of route
login_manager.login_message_category = 'info'
# CORS()
mail = Mail()



def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    CORS(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app