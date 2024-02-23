from flask import(Blueprint, flash, g, redirect, render_template, request, session, url_for)
from wmgzon.db import get_db

from wmgzon.auth import login_required

admin_bp = Blueprint('adminpage', __name__, url_prefix='/admin')

@admin_bp.route('/create', methods=('GET', 'POST'))
@login_required
def create_product():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        error = None

        if not title:
            error = 'Title is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO product (title, price, author_id)'
                ' VALUES (?, ?, ?)',
                (title, price, g.user['id'])
            )
            db.commit()
            flash('product created')
            return redirect(url_for('landingpage.index'))

    return render_template('admin/add_product.html')


