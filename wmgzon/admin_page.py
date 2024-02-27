from flask import(current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for)
from wmgzon.db import get_db
import os
from werkzeug.utils import secure_filename
from wmgzon.auth import login_required
from wmgzon import current_app

admin_bp = Blueprint('adminpage', __name__, url_prefix='/admin')

# Function to check if the file extension is allowed
def allowed_file(filename):
    #ALLOWED_EXTENSIONS = current_app.config['ALLOWED_EXTENSIONS']
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/create', methods=('GET', 'POST'))
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

@admin_bp.route('/<int:id>/delete', methods=('POST'))
@login_required
def delete(id)