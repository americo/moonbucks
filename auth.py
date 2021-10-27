from flask import Blueprint, render_template, redirect, url_for, request, flash, request
from flask_login.utils import logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Comment
from flask_login import login_user
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        # check if user actually exists
        # take the user supplied password, hash it, and compare it to the hashed password in database
        if not user or not check_password_hash(user.password, password):
            return render_template('login.html', login_failed=True)    
        
        login_user(user, remember=False)

        return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        fullname = request.form.get('full_name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user: # if a user is found, we want to redirect back to register page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.register'))

        user = User.query.filter_by(username=username).first()
        if user: # if a user is found, we want to redirect back to register page so user can try again
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        new_user = User(name=fullname ,email=email, username=username, password=generate_password_hash(password, method='sha256'), avatar_url="avatar.png", cover_url='cover.png')

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))