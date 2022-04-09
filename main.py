from flask import Flask
from flask_restx import Api
from config import DevConfig
from extension import db
from models import Recipe, User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from auth import auth_ns
from recipe import recipe_ns

def create_app(config):
    # flask app creation
    app = Flask(__name__)
    # database configuration
    db.init_app(app)
    migrate = Migrate(app,db)
    # setting configuration
    app.config.from_object(config)
    # jwt configuration
    JWTManager(app)
    # api configuration
    api = Api(app,doc='/docs',version='2.1', title='Flask API',
    description='Recipe App',)

    api.add_namespace(auth_ns)
    api.add_namespace(recipe_ns)


    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "Recipe":Recipe,
            "User":User
        }

    return app




