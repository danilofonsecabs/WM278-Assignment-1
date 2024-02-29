from flask import Flask, render_template, current_app
import sqlite3
from markupsafe import escape
import os




def create_app(test_config=None):
    # create and configure the app
    UPLOAD_FOLDER = 'wmgzon/static/images'  # Define the upload folder
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    app = Flask(__name__,static_folder='static', instance_relative_config=True)
    with app.app_context():
        app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'wmgzon.sqlite'),
             # Define allowed extensions

        )
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    @app.route("/hello")
    def home():
        return "Hello! this is checking wether the website is functional <h1>HELLO</h1>"

    @app.route('/view_data')
    def view_data():
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute('SELECT * FROM product')
        data = c.fetchall()
        conn.close()
        return render_template('view_data_product.html', data=data)

    @app.route('/view_data_grocery')
    def view_data_grocery():
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute('SELECT * FROM category')
        data = c.fetchall()
        conn.close()
        return render_template('view_data_category.html', data=data)

    @app.route('/view_data_stock')
    def view_data_stock():
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute('SELECT * FROM stock_information')
        data = c.fetchall()
        conn.close()
        return render_template('view_data_stock.html', data=data)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import grocery
    app.register_blueprint(grocery.grocery)

    from . import landingpage
    app.register_blueprint(landingpage.landingpage)
    app.add_url_rule('/', endpoint='index')

    from . import admin_page
    app.register_blueprint(admin_page.admin_bp)




    return app