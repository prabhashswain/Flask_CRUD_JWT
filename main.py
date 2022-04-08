from flask import Flask
from flask_restx import Api,Resource
from config import DevConfig
from extension import db
from models import Recipe
# flask app creation
app = Flask(__name__)
# database configuration
db.init_app(app)
# setting configuration
app.config.from_object(DevConfig)
# api configuration
api = Api(app,doc='/docs')

@api.route('/hello')
class index(Resource):
    def get(self):
        return {'msg':'Hello Flask'}

@app.shell_context_processor
def make_shell_context():
    return {
        "db":db,
        "Recipe":Recipe,
    }


if __name__ == "__main__":
    app.run()


