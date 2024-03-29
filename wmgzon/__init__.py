from flask import Flask, render_template, current_app, request
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
    def hello():
        return 'Hello, World!'

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