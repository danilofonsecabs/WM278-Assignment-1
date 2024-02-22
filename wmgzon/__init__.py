from flask import Flask, render_template
import sqlite3
from markupsafe import escape
import os


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'wmgzon.sqlite'),
    )

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
        return "Hello! this is the main page <h1>HELLO</h1>"

    @app.route('/view_data')
    def view_data():
        conn = sqlite3.connect(app.config['DATABASE'])
        c = conn.cursor()
        c.execute('SELECT * FROM user')
        data = c.fetchall()
        conn.close()
        return render_template('view_data.html', data=data)




    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import grocery
    app.register_blueprint(grocery.grocery)

    from . import landingpage
    app.register_blueprint(landingpage.landingpage)
    app.add_url_rule('/', endpoint='index')



    return app