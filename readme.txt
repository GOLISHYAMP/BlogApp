
write like this in the shell 
from flaskblog import app, db
>>> from flaskblog import User, Post
>>> with app.app_context():
...     User.query.all()
User.query.first()
User.query.filter_by(username='sai').all()
User.query.filter_by(username='sai').first()
user = User.query.get(1)   # this is to get the user by id

from flaskblog import app, db
>>> with app.app_context():
...     db.create_all()
...     print("Database tables created.")



write like this in iteractive cli
 with app.app_context():                                               
...     post1 = Post(title="blog1", content="first post content", user_id=user.id)
...     post2 = Post(title="blog2", content="second post content", user_id=user.id)
...     db.session.add(post1) 
...     db.session.add(post2)                                             
...     db.session.commit()   

>>> with app.app_context():       
...     post = Post.query.first()
...     post.author  

 with app.app_context():
...     db.drop_all()       
...


##### This is for hashing the password
##### We cannot store the plain text directly in the database.
#### pip install flask_bcrypt

>>> from flask_bcrypt import Bcrypt
>>> bcrypt = Bcrypt()
hashed_pwd = bcrypt.generate_password_hash("helloworld").decode('utf-8')
bcrypt.check_password_hash(hashed_pwd, "helloworld")


##### flask-login
The load_user function in a Flask application using Flask-Login
 is essential for handling user sessions and managing user authentication. 
 Here's an in-depth explanation of its components and functionality:

Components and Functionality
Imports and Setup:

python
Copy code
from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin

db is typically a SQLAlchemy instance for database operations.
login_manager is an instance of LoginManager from Flask-Login,
 used for session management.
datetime is used for handling date and time, often for timestamps in user models.

UserMixin is a Flask-Login mixin that provides default implementations 
for methods that Flask-Login expects user objects to have, 
such as is_authenticated, is_active, is_anonymous, and get_id.

User Model:
Your user model (not shown but implied) should inherit from SQLAlchemy's model class and UserMixin. For example:

python
Copy code
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # other fields such as username, email, password, etc.
The load_user Function:

python
Copy code
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
The @login_manager.user_loader decorator registers the load_user 
function with Flask-Login.
This function is called by Flask-Login to load a user from the session. 
Flask-Login uses this to reload the user object from the user ID stored
 in the session cookie.

How It Works
Session Management:
When a user logs in, their user ID is stored in the session.
Flask-Login uses this user ID to retrieve the user's data when needed.

User Loader Function:

When Flask-Login needs to load the user (e.g., for checking 
authentication status, accessing user-specific data),
 it calls the load_user function.
The load_user function receives the user ID (as a string) from the session cookie.
It queries the database for the user with that ID using
User.query.get(int(user_id)).
This converts the user_id to an integer and fetches the user object from the database.
Methods Provided by UserMixin
is_authenticated: Returns True if the user is authenticated,
 i.e., they have provided valid credentials.
is_active: Returns True if the user's account is active.
is_anonymous: Returns True if the user is not authenticated.
get_id: Returns the unique ID of the user as a string 
(used to store in the session cookie).

PAGINATION:

>>> from flaskblog import app, db
>>> from flaskblog.models import User, Post
>>> with app.app_context():
...     User.query.all()
...
[user ( 'Ram', 'Ram@gmail.com', 'fc28560385a6f8a9WIN_20240606_21_07_09_Pro.jpg'),
 user ( 'Vigneshsallagiri ', 'sallagirivignesh@gmail.com', 'default.jpg'),
  user ( 'SaiG', 'golisaikrushna@gmail.com', 'default.jpg'), 
  user ( 'Sai', 'sai@gmail.com', '2d16826086b919ecWIN_20240101_13_32_51_Pro.jpg'),
   user ( 'vinod', 'vinod@gmail.com', '7019e18fa93a6f732car.jpg')]
>>> with app.app_context():
...     users = User.query.paginate()
... 
>>> DIR(users)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'DIR' is not defined. Did you mean: 'dir'?
>>> dir(users)
['__class__', '__delattr__', '__dict__', '__dir__', 
'__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', 
'__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', 
'__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
 '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
  '__weakref__', '_prepare_page_args', '_query_args', '_query_count', 
  '_query_items', '_query_offset', 'first', 'has_next', 'has_prev', 'items',
   'iter_pages', 'last', 'max_per_page', 'next', 'next_num', 'page',
    'pages', 'per_page', 'prev', 'prev_num', 'total']
>>> users.page()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'int' object is not callable
>>> users.page  
1
>>> users.pages
1
>>> users.total
5
>>> users.max_per_page
>>> users.iter_pages
<bound method Pagination.iter_pages of 
<flask_sqlalchemy.pagination.QueryPagination object at 0x0000022942407CD0>>
>>> for page in users.iter_pages:
...     print(page)
...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'method' object is not iterable
>>> users.iter_pages:             
  File "<stdin>", line 1
    users.iter_pages:
                     ^
SyntaxError: invalid syntax
>>> users.iter_pages 
<bound method Pagination.iter_pages of 
<flask_sqlalchemy.pagination.QueryPagination object at 0x0000022942407CD0>>
>>> users.per_page
20
>>> for post in users.items:
...     print(post)
...
user ( 'Ram', 'Ram@gmail.com', 'fc28560385a6f8a9WIN_20240606_21_07_09_Pro.jpg')    
user ( 'Vigneshsallagiri ', 'sallagirivignesh@gmail.com', 'default.jpg')
user ( 'SaiG', 'golisaikrushna@gmail.com', 'default.jpg')
user ( 'Sai', 'sai@gmail.com', '2d16826086b919ecWIN_20240101_13_32_51_Pro.jpg')    
user ( 'vinod', 'vinod@gmail.com', '7019e18fa93a6f732car.jpg')
>>> with app.app_context():
...     posts = Post.query.paginate()     
...
>>> for post in posts.items:
...     print(post)
...
post ( 'first updated post done!!!', '2024-06-24 00:36:11.802976')
post ( 'my second post', '2024-06-23 23:35:58.674594')
post ( 'Ram1', '2024-07-01 22:08:08.768848')
post ( 'Ram2', '2024-07-01 22:08:26.314505')
post ( 'Ram3', '2024-07-01 22:09:21.917780')
post ( 'Ram4', '2024-07-01 22:09:45.828689')
post ( 'Ram5', '2024-07-01 22:10:05.458018')
post ( 'Ram6', '2024-07-01 22:10:22.020154')
post ( 'Ram7', '2024-07-01 22:10:36.990488')
post ( 'Ram8', '2024-07-01 22:10:52.423928')
post ( 'Ram9', '2024-07-01 22:11:17.032330')
post ( 'Ram12', '2024-07-01 22:11:34.189255')
post ( 'Ram10', '2024-07-01 22:12:59.263139')
post ( 'Ram11', '2024-07-01 22:13:12.792034')
post ( 'Ram13', '2024-07-01 22:13:36.486175')
post ( 'Ram14', '2024-07-01 22:13:57.695245')
post ( 'Ram15', '2024-07-01 22:14:18.452007')
post ( 'Ram16', '2024-07-01 22:14:34.027837')
post ( 'Ram17', '2024-07-01 22:14:46.995834')
post ( 'Ram18', '2024-07-01 22:15:01.349413')
>>> with app.app_context():
...     posts = Post.query.paginate(page=2)
...
>>> for post in posts.items:
...     print(post)
...
post ( 'Ram19', '2024-07-01 22:15:16.531773')
post ( 'Ram20', '2024-07-01 22:15:48.281146')
post ( 'Sai3', '2024-07-01 22:16:46.856187')
post ( 'Ram4', '2024-07-01 22:17:03.275039')
post ( 'Sai5', '2024-07-01 22:17:21.088847')
>>> posts.total
25
>>> users.total
5
>>>

##########################################################
Secret key validation with respect to time

>>> from itsdangerous import URLSafeTimedSerializer as Serializer
>>> s =  Serializer('secret')
>>> token = s.dumps({'user_id': 123})
>>> s.loads(token)
{'user_id': 123}
>>> s.loads(token,5)