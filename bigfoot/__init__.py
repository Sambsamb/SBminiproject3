import os

from flask import Flask


# The application factory
def create_app(test_config=None):
    # create and configure the app
    # tells the app that configuration files are relative to the instance folder
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'bigfoot.sqlite'),
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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Import and call db.init_app(app) function from the factory
    from . import db
    db.init_app(app)

    # Import and register the auth blueprint from the factory
    from . import auth
    app.register_blueprint(auth.bp)

    # Import and register the blog blueprint from the factory
    from . import blog
    app.register_blueprint(blog.bp)
    # Unlike the auth blueprint, the blog blueprint does not have a url_prefix. So the index view will be at /,
    # the create view at /create, and so on. The blog is the main feature of Flaskr, so it makes sense that the
    # blog index will be the main index.
    app.add_url_rule('/', endpoint='index')

    return app


