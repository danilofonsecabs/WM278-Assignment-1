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
    return render_template('landingpage/grocery.html', products=products, page_type='all')

@grocery.route('/grocery_gluten_free')
def grocery_gluten_free():
    db = get_db()
    gluten_free_products = db.execute(
        'SELECT p.id, p.title, p.description, p.price, p.image_filename, p.author_id, u.username '
        'FROM product p '
        'JOIN user u ON p.author_id = u.id '
        'JOIN grocery g ON p.id = g.product_id '
        'WHERE g.gluten_free = 1'  # Select products where gluten_free is true
    ).fetchall()
    return render_template('landingpage/grocery.html', products=gluten_free_products, page_type='gluten_free')

@grocery.route('/grocery_vegan')
def grocery_vegan():
    db = get_db()
    vegan_products = db.execute(
        'SELECT p.id, p.title, p.description, p.price, p.image_filename, p.author_id, u.username '
        'FROM product p '
        'JOIN user u ON p.author_id = u.id '
        'JOIN grocery g ON p.id = g.product_id '
        'WHERE g.vegan = 1'  # Select products where gluten_free is true
    ).fetchall()
    return render_template('landingpage/grocery.html', products=vegan_products, page_type='vegan')

@grocery.route('/grocery_baby_foods')
def grocery_baby_foods():
    db = get_db()
    baby_foods = db.execute(
        'SELECT p.id, p.title, p.description, p.price, p.image_filename, p.author_id, u.username '
        'FROM product p '
        'JOIN user u ON p.author_id = u.id '
        'JOIN grocery g ON p.id = g.product_id '
        'WHERE g.baby_foods = 1'  # Select products where gluten_free is true
    ).fetchall()
    return render_template('landingpage/grocery.html', products=baby_foods, page_type='baby_foods')

@grocery.route('/grocery_bestseller')
def grocery_bestseller():
    db = get_db()
    bestseller = db.execute(
        'SELECT p.id, p.title, p.description, p.price, p.image_filename, p.author_id, u.username '
        'FROM product p '
        'JOIN user u ON p.author_id = u.id '
        'JOIN grocery g ON p.id = g.product_id '
        'WHERE g.bestseller = 1'  # Select products where gluten_free is true
    ).fetchall()
    return render_template('landingpage/grocery.html', products=bestseller, page_type='bestseller')

@grocery.route('/grocery_beer_wine')
def grocery_beer_wine():
    db = get_db()
    beer_wine = db.execute(
        'SELECT p.id, p.title, p.description, p.price, p.image_filename, p.author_id, u.username '
        'FROM product p '
        'JOIN user u ON p.author_id = u.id '
        'JOIN grocery g ON p.id = g.product_id '
        'WHERE g.beer_wine = 1'  # Select products where gluten_free is true
    ).fetchall()
    return render_template('landingpage/grocery.html', products=beer_wine, page_type='beer_wine')

@grocery.route('/grocery_frozen')
def grocery_frozen():
    db = get_db()
    frozen = db.execute(
        'SELECT p.id, p.title, p.description, p.price, p.image_filename, p.author_id, u.username '
        'FROM product p '
        'JOIN user u ON p.author_id = u.id '
        'JOIN grocery g ON p.id = g.product_id '
        'WHERE g.frozen = 1'  # Select products where gluten_free is true
    ).fetchall()
    return render_template('landingpage/grocery.html', products=frozen, page_type='frozen')

@grocery.route('/grocery_home_care')
def grocery_home_care():
    db = get_db()
    home_care = db.execute(
        'SELECT p.id, p.title, p.description, p.price, p.image_filename, p.author_id, u.username '
        'FROM product p '
        'JOIN user u ON p.author_id = u.id '
        'JOIN grocery g ON p.id = g.product_id '
        'WHERE g.home_care = 1'  # Select products where gluten_free is true
    ).fetchall()
    return render_template('landingpage/grocery.html', products=home_care, page_type='home_care')


@grocery.route('/grocery_food_cupboard')
def grocery_food_cupboard():
    db = get_db()
    food_cupboard = db.execute(
        'SELECT p.id, p.title, p.description, p.price, p.image_filename, p.author_id, u.username '
        'FROM product p '
        'JOIN user u ON p.author_id = u.id '
        'JOIN grocery g ON p.id = g.product_id '
        'WHERE g.food_cupboard = 1'  # Select products where gluten_free is true
    ).fetchall()
    return render_template('landingpage/grocery.html', products=food_cupboard, page_type='food_cupboard')


@grocery.route('/grocery_dairy_free')
def grocery_dairy_free():
    db = get_db()
    dairy_free_products = db.execute(
        'SELECT p.id, p.title, p.description, p.price, p.image_filename, p.author_id, u.username '
        'FROM product p '
        'JOIN user u ON p.author_id = u.id '
        'JOIN grocery g ON p.id = g.product_id '
        'WHERE g.dairy_free = 1'  # Select products where gluten_free is true
    ).fetchall()
    return render_template('landingpage/grocery.html', products=dairy_free_products, page_type='dairy_free')

@grocery.route('/<int:product_id>')
def view_product(product_id):
    # Retrieve product information from the database using the product_id
    print("this is product id ", product_id)
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

