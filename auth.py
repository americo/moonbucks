from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Task
from flask_login import login_user
from app import db

auth = Blueprint('auth', __name__)