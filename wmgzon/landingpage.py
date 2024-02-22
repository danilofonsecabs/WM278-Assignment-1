from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
import sqlite3
from wmgzon.auth import login_required
from wmgzon.db import get_db

landingpage = Blueprint('landingpage', __name__, url_prefix="/home")

@landingpage.route('/')
def index():
    db = get_db()
    # posts = db.execute(
    #     'SELECT p.id, title, body, created, author_id, username'
    #     ' FROM post p JOIN user u ON p.author_id = u.id'
    #     ' ORDER BY created DESC'
    # ).fetchall()
    return render_template('landingpage/index.html')

# @landingpage.route('/view_data')
# def view_data():
#     conn = sqlite3.connect('wmgzon.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM user')
#     data = c.fetchall()
#     conn.close()
#     return render_template('view_data.html', data=data)
#
#
#
