from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from demo.config import Config
from flask_restful import Api


# Adding flask extensions for SQLAlchemy, BCrypt and Flask Restful 
db = SQLAlchemy()
bcrypt = Bcrypt()
api = Api()


# Function to create flask app using our config
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Import and register our blueprints
    from demo.users.routes import users
    from demo.apis.routes import apis
    from demo.main.routes import main
    from demo.errors.handlers import errors
    app.register_blueprint(users)
    api.init_app(apis)
    app.register_blueprint(apis)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # Return flask app
    return app
