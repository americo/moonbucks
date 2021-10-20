import os
from flask import Blueprint, render_template, request, url_for, redirect, flash, Flask, abort, send_from_directory
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Comment
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/product/<id>')
def product(id):
    return render_template('product.html')