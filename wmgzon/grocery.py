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

