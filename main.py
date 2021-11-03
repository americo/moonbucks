import os
import uuid
from flask import Blueprint, render_template, request, url_for, redirect, flash, Flask, abort, send_from_directory
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import Product, User, Comment
from app import db

from xml.dom import minidom
from lxml import etree

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg'}
ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/jpg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 2)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    products = Product.query.all()
    all_products = []
    for product in products:
        all_products.append(product)

    print(type(all_products))
    return render_template('index.html', products=all_products)

@main.route('/search')
def search():
    searchQuery = request.args.get('q', '')

    if searchQuery:
        products = Product.query.all()
        all_products = []
        for product in products:
            if searchQuery in product.name:
                all_products.append(product)
            elif searchQuery in product.subtitle:
                all_products.append(product)
            elif searchQuery in product.description:
                all_products.append(product)
            else:
                pass
        return render_template('index.html', products=all_products, hasSearchQuery=True, searchQuery=searchQuery)
    else:
        return render_template('index.html')

@main.route('/format')
def productFormat():
    formatQuery = request.args.get('q', '')
    if formatQuery == "MOÍDO":
            formatQuery == "MOIDO"

    class Product:
            def __init__(self, id, user_id, name, subtitle, description, p_format, image_url):
                self.id = id
                self.user_id = user_id
                self.name = name
                self.subtitle = subtitle
                self.descritpion = description
                self.p_format = p_format
                self.image_url = image_url

    if formatQuery:
        query = db.engine.execute(f"SELECT * FROM Product WHERE p_format == '{formatQuery}'")
        products = []
        for q in query:
                p1 = Product(q[0], q[1], q[2], q[3], q[4], q[5], q[6])
                products.append(p1)

        all_products = []
        for product in products:
            all_products.append(product)

    if "SELECT" in formatQuery.upper():
        return render_template('index.html', products=all_products, hasSQLiPayload=True)
    elif "UNION" in formatQuery.upper():
        return render_template('index.html', products=all_products, hasSQLiPayload=True)
    else:
        return render_template('index.html', products=all_products)

@main.route('/product/<id>')
def product(id):
    product = Product.query.filter_by(id=id).first()
    user = User.query.filter_by(id=product.user_id).first()

    comments = Comment.query.filter_by(product_id=id)
    all_comments = []
    for comment in comments:
        all_comments.append(comment)

    users = User.query.all()
    all_users = []
    for user1 in users:
        all_users.append(user1)
    return render_template('product.html', product=product, user=user, comments=all_comments, users=users)

@main.route('/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'GET':
        return render_template('add-product.html')
    else:
        name = request.form.get('name')
        subtitle = request.form.get('subtitle')
        description = request.form.get('description')
        p_format = request.form.get('p_format')

        if p_format == "MOÍDO":
            p_format == "MOIDO"

        file = request.files['file']

        if file != '':
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                try:
                    ext = filename.split('.')[2]
                except:
                    ext = filename.split('.')[1]
                filename = "%s.%s" % (uuid.uuid4(), ext)
                file.save(os.path.join('./images/product', filename))
            else:
                return "<h3>Extensão não permitida.</h3>"

        new_product = Product(user_id=current_user.id, name=name, subtitle=subtitle, description=description, p_format=p_format, image_url=filename)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('main.account'))

@main.route('/product/delete/<id>')
@login_required
def remove_product(id):
    product = Product.query.filter_by(id=id).first()
    if product:
        db.session.delete(product)
        db.session.commit()

        image_url = product.image_url
        os.system(f"rm ./images/product/{image_url}")
    
    return redirect(url_for('main.account'))

@main.route('/comment/add', methods=['POST'])
def add_comment():
    user_id = request.form.get('user_id')
    product_id = request.form.get('product_id')
    subject = request.form.get('subject')
    comment = request.form.get('comment')

    new_comment = Comment(user_id=user_id, product_id=product_id, subject=subject, body=comment)
    db.session.add(new_comment)
    db.session.commit()

    if user_id != current_user.id:
        flag = "FLAG: $TBH#eTzYn5L3s7fsPgAD"
        return render_template('flag.html', flag=flag)

    return redirect(url_for('main.product', id=product_id))

@main.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    file = ''
    if request.method == "GET":
        products = Product.query.filter_by(user_id=current_user.id)
        all_products = []
        for product in products:
            all_products.append(product)
        return render_template('account.html', products=all_products)
    else:
        fullname = request.form.get('full_name')
        email = request.form.get('email')
        username = request.form.get('username')
        try:
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            file = request.files['file']
        except:
            pass

        user = User.query.filter_by(email=current_user.email).first()

        exist_user = User.query.filter_by(email=email).first()
        if email != current_user.email:
            if exist_user:
                flash('Email address already exists')
                return redirect(url_for('main.account'))

        exist_user = User.query.filter_by(username=username).first()
        if username != current_user.username:
            if exist_user:
                flash('Username already exists')
                return redirect(url_for('main.account'))

        if current_password and new_password:
            if not user or not check_password_hash(user.password, current_password):
                return render_template('login.html', login_failed=True)
            user.password = generate_password_hash(new_password, method='sha256')

        if file != '':
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                filename = file.filename
                try:
                    file.save(os.path.join('./images/profile', filename))
                except:
                    pass
                
            if user.avatar_url != 'profile.png':
                    os.system(f"rm ./images/profile/{user.avatar_url}")
            user.avatar_url = filename

        user.name = fullname
        user.email = email
        user.username = username
        db.session.commit()

        return redirect(url_for('main.account'))

@main.route('/account/cover', methods=['POST'])
@login_required
def account_cover():
    if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
    file = request.files['file']

    user = User.query.filter_by(email=current_user.email).first()

    if file != '':
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                mimetype = file.content_type
                if mimetype in ALLOWED_MIME_TYPES:
                    filename = secure_filename(file.filename)
                    ext = filename.split('.')[-1]
                    filename = "%s.%s" % (uuid.uuid4(), ext)
                    file.save(os.path.join('./images/profile', filename))
                else:
                    return "<h3>MIME-TYPE não permitido.</h3>"
                
            if user.cover_url != 'cover.png':
                    os.system(f"rm ./images/profile/{user.cover_url}")
            user.cover_url = filename
    
    db.session.commit()

    return redirect(url_for('main.account'))

@main.route('/profile/<id>')
def profile(id):
    user = User.query.filter_by(id=id).first()

    products = Product.query.filter_by(user_id=user.id)
    all_products = []
    for product in products:
        all_products.append(product)
    return render_template('profile.html', user=user, products=all_products)

@main.route('/images/profile/<filename>')
def load_profile_image(filename):
    try:
        file = open(f"./images/profile/{filename}")
        file_data = file.read()
        xml = file_data
        parser = etree.XMLParser(no_network=False)
        doc = etree.tostring(etree.fromstring(str(xml), parser))
        return doc
    except:
        return send_from_directory('./images/profile', filename), 200

@main.route('/images/product/<filename>')
def load_product_image(filename):
    return send_from_directory('./images/product', filename), 200

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/.git/<path:path>')
def git(path):
    return send_from_directory(".git", path)

# @main.route('/insert')
# def insert():
#     db.engine.execute("ALTER TABLE comment ADD product_id int;")
#     return "X"