from flaskblog import db, login_manager, Serializer #,app
from datetime import datetime
from flask_login import UserMixin
from flask import current_app
# now this UserMixin extension have the is_authenticated, is_active ,
#  is_anonymous, get_id

# This description is given in the readme file
# Basically it is used by the login manager to find to fetch userdata
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id':self.id})

    #Static methods are useful for creating methods that 
    # logically belong to a class but do not need access 
    # to the class or instance-specific data. 
    # They are good for utility functions and operations
    #  that are self-contained.

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=1800)  # Specify max_age here
        except Exception as e:
            print(f"Error decoding token: {e}")
            return None
        return User.query.get(user_id['user_id'])

    def __repr__(self):
        return f"user ( '{self.username}', '{self.email}', '{self.image_file}')"
    


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False) 
    # Here smallcase table user and column id, by default model name converts
    # into table name with smallcase.

    def __repr__(self):
        return f"post ( '{self.title}', '{self.date_posted}')"