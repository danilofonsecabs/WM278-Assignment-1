from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import sqlite3
from wmgzon.auth import login_required
from wmgzon.db import get_db

landingpage = Blueprint('landingpage', __name__)

@landingpage.route('/')
def index():

    db = get_db()
    products = db.execute(
            'SELECT p.id, title, description, price, image_filename, author_id, username'
            ' FROM product p JOIN user u ON p.author_id = u.id'
            ' ORDER BY price DESC'

        ).fetchall()


    return render_template('landingpage/index.html', products=products)

@landingpage.route('/search')
def search():
    db = get_db()
    query = request.args.get('query', '')
    results = db.execute(
    'SELECT * FROM product WHERE title LIKE ?', ('%' + query + '%',)
    ).fetchall()
    return render_template('search_results.html', results=results)


@landingpage.route('/toys')
def index_toys():
    return render_template('landingpage/Coming_soon_products.html', page_type='toys')

@landingpage.route('/electrical')
def index_electrical():
    return render_template('landingpage/Coming_soon_products.html', page_type='electrical')
