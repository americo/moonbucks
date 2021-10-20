from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Comment
from flask_login import login_user
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')