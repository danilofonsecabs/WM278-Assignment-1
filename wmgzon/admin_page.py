from flask import(current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for)
from wmgzon.db import get_db
import os
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort
from wmgzon.auth import login_required
from wmgzon import current_app


admin_bp = Blueprint('adminpage', __name__)

# Function to check if the file extension is allowed
def allowed_file(filename):

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@admin_bp.route('/adminhome', methods=('GET', 'POST'))
@login_required
def admin_home():
    return render_template('admin/adminpage.html')


@admin_bp.route('/createproduct', methods=('GET', 'POST'))
@login_required
def create_product():
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']
        error = None
        print("post")

        # File Upload Handling
        if 'image' not in request.files:
            #print('no file part')
            flash('No file part')
            return redirect(request.url)

        file = request.files['image']


        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
            #print('nofile')

        if file and allowed_file(file.filename):
            print(UPLOAD_FOLDER)
            print(file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        else:
            flash('Invalid file format')
            return redirect(request.url)

        # Database Handling
        if not title:
            error = 'Title is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO product (title, price, description, image_filename, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, price, description, filename, g.user['id'])
            )
            db.commit()
            flash('Product created')
            return redirect(url_for('landingpage.index'))

    return render_template('admin/add_product.html')


@admin_bp.route('/view_products')
@login_required
def view_products_admin():
    db = get_db()
    products = db.execute(

        'SELECT p.id, title, description, price, image_filename, author_id, username'
        ' FROM product p JOIN user u ON p.author_id = u.id'
        ' ORDER BY price DESC'

     ).fetchall()
    return render_template('admin/view_products_admin.html', products=products)

@admin_bp.route('/<int:product_id>')
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


@admin_bp.route('/<int:product_id>/delete', methods=('POST','GET'))
@login_required
def delete(product_id):
    get_product(product_id)
    print(product_id)
    db = get_db()
    db.execute('DELETE FROM product WHERE id = ?', (product_id,))
    db.commit()
    return redirect(url_for('adminpage.view_products_admin'))

@admin_bp.route('/<int:product_id>/update', methods=('GET', 'POST'))
@login_required
def update(product_id):

    product = get_product(product_id)

    print("product_ id", product_id)
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']
        author_id = g.user['id']
        error = None


        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE product SET title = ?, price = ?, description = ?, author_id = ?'
                ' WHERE id = ?',
                (title, price, description, author_id, product_id)
            )
            db.commit()
            flash('Product edited')
            return redirect(url_for('adminpage.view_products_admin'))

    return render_template('admin/update.html', product=product)
