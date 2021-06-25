from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.models import User
from app import db

auth = Blueprint('auth', __name__, template_folder="../views/templates")


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Bad signup.', 'success')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()
    flash('Success signup.', 'success')
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Bad login.', 'error')
        return redirect(url_for('auth.login'))
    login_user(user, remember=True)
    flash('Success login.', 'success')
    return redirect(url_for('user.user_me', name=user.name, email=user.email))


@auth.route('/logout')
def logout():
    logout_user()
    flash('Success logout.', 'success')
    return redirect(url_for('auth.login'))