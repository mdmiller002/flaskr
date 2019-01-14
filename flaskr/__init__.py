import os
from flask import Flask

def create_app(test_config=None):
    """Create the Flask app"""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # Load custom configuration, or test configuration
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure instance directory exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # URL mappings
    @app.route('/hello')
    def hello():
        return 'Hello world'

    # Initialize the database
    from . import db
    db.init_app(app)

    # Register authentication blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # Register blog blueprint
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
