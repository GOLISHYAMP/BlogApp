import os
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm,
                              UpdateAccountForm,
                              RequestResetForm, ResetPasswordForm)
from flaskblog import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode(
            'utf-8')
        user = User(username = form.username.data, email = form.email.data, 
                    password = hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created!, now you can login', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login Successful !', 'success')
            next = request.args.get('next')
            return redirect(next) if next else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            if current_user.image_file != 'default.jpg':
                # Delete the previous profile pic from the database
                # Construct the file path
                file_path = os.path.join(users.root_path, 'static/profile_pics',
                                        current_user.image_file)
                # Check if the file exists before attempting to delete it
                if os.path.exists(file_path):
                    os.remove(file_path)

            picture_file_name = save_picture(form.picture.data)
            current_user.image_file = picture_file_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your profile has been updated!",'success')
        return redirect(url_for('users.account'))
    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/'+ 
                         current_user.image_file)
    return render_template('account.html',title="Account", 
                           image_file = image_file,form = form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author = user)\
        .order_by(Post.date_posted.desc())\
            .paginate(per_page = 5, page = page)
    return render_template('user_posts.html', posts=posts, user = user)



@users.route("/reset_password", methods = ["GET", "POST"])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash("An email is sent with instructions to reset your password",'info')
        return redirect(url_for('users.login'))
    return render_template('request_reset.html', form = form, 
                           title='Reset Password')

@users.route("/reset_password/<token>", methods = ["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    print("USER")
    print(user)
    if user is None:
        flash("Invalid or expired token",'warning')
        return redirect(url_for('users.request_reset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode(
            'utf-8')
        user.password = hashed_pwd
        db.session.commit()
        flash(f'Password changed successfully!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form = form, title='Reset Password')

