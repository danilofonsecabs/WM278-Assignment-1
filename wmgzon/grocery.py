from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from wmgzon.auth import login_required
from wmgzon.db import get_db

grocery = Blueprint('grocery', __name__, template_folder='landingpage/grocery')

@grocery.route('/grocery')
def index():
    db = get_db()
    products = db.execute(
        'SELECT p.id, title, description, price, image_filename, author_id, username '
        'FROM product p '
        'JOIN user u ON p.author_id = u.id '
        'JOIN category c ON p.id = c.product_id '
        'WHERE c.category = "grocery" '
        'ORDER BY p.price DESC'
    ).fetchall()
    return render_template('landingpage/grocery.html', products=products)

@grocery.route('/<int:product_id>')
def view_product(product_id):
    # Retrieve product information from the database using the product_id
    cursor = get_db().cursor()  # Assuming you have a function get_db() to get a database cursor

    # Execute SQL query to fetch product details
    cursor.execute(
            'SELECT p.id, p.title, p.price, p.description, p.image_filename'
            ' FROM product p'
            ' WHERE p.id = ?',
            (product_id,))

    product = cursor.fetchone()

    # If product is not found, return a 404 error
    if product is None:
        abort(404)

    # Pass the product information to the product detail template
    return render_template('landingpage/product_detail.html', product=product)


def get_product(id, check_author=True):
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

