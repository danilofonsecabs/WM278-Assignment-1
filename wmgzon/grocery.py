from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from wmgzon.auth import login_required
from wmgzon.db import get_db

grocery = Blueprint('grocery', __name__, url_prefix='/home', template_folder='landingpage/grocery')

@grocery.route('/grocery')
def index():
    db = get_db()
    products = db.execute(
         # 'SELECT p.id, title, body, created, author_id, username'
         # ' FROM post p JOIN user u ON p.author_id = u.id'
         # ' ORDER BY created DESC'
        'SELECT p.id, title, description, price, image_filename, author_id, username'
        ' FROM product p JOIN user u ON p.author_id = u.id'
        ' ORDER BY price DESC'

     ).fetchall()
    return render_template('landingpage/grocery.html', products=products)

@grocery.route('/product/<int:product_id>')
def view_product(product_id):
    # Retrieve product information from the database using the product_id
    product= get_db().execute(
        'SELECT p.id, title, description, price, image_filename, author_id, username'
        ' FROM product p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = product_id',
        (id,)
    ).fetchone()
    # Pass the product information to the product detail template
    return render_template('landingpage/product_detail.html', product=product_id)
def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, description, price, image_filename, author_id, username'
        ' FROM product p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"product id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

