from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    avatar_url = db.Column(db.String(100))
    cover_url = db.Column(db.String(100))

class Comment(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    subject = db.Column(db.String(10000))
    body = db.Column(db.String(10000))

class Product(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String(1000))
    subtitle = db.Column(db.String(1000))
    description = db.Column(db.String(1000))
    p_format = db.Column(db.String(1000))
    image_url = db.Column(db.String(1000))