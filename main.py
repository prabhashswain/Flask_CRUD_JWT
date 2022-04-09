from os import access
from flask import Flask,request,jsonify
from flask_restx import Api,Resource,fields
from config import DevConfig
from extension import db
from models import Recipe, User
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,jwt_required

# flask app creation
app = Flask(__name__)
# database configuration
db.init_app(app)
migrate = Migrate(app,db)
# setting configuration
app.config.from_object(DevConfig)
# jwt configuration
JWTManager(app)
# api configuration
api = Api(app,doc='/docs')


# model serializer
recipe_model = api.model('Recipe',{
    "id":fields.Integer(),
    "name":fields.String(),
    "description":fields.String()
})

signup_model = api.model('Signup',{
    "username":fields.String(),
    "email":fields.String(),
    "password":fields.String()
})

login_model = api.model('Login',{
    "username":fields.String(),
    "password":fields.String()
})

@api.route("/signup")
class SignUpResource(Resource):
    @api.expect(signup_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        print(user)
        if user:
            return jsonify({'error':f"Username {username} Already Taken"},401)

        new_user = User(
            username = username,
            email = data.get('email'),
            password = generate_password_hash(password)
        )
        new_user.save()
        return jsonify({'msg':'User created successfully!!!'},201)

@api.route("/login")
class LoginResource(Resource):
    @api.expect(login_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        # filter user from db
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password,password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            return jsonify(
                {'acess_token':access_token,'refresh_token':refresh_token}
            )
        else:
            return jsonify({'error':"Invalid Credentials"})


@api.route('/recipes')
class RecipeResource(Resource):
    @api.marshal_list_with(recipe_model)
    @jwt_required()
    def get(self):
        """Get all recipes"""
        recipes = Recipe.query.all()
        return recipes

    @api.marshal_with(recipe_model)
    @api.expect(recipe_model)
    @jwt_required()
    def post(self):
        """Post a recipe"""
        data = request.get_json()
        new_recipe = Recipe(
            name = data.get('name'),
            description = data.get('description')
        )
        new_recipe.save()
        return new_recipe,201

@api.route('/recipe/<int:id>')
class RecipeResource(Resource):
    @api.marshal_with(recipe_model)
    @jwt_required()
    def get(self,id):
        """Get a particular Recipe"""
        recipe = Recipe.query.filter_by(id=id).first()
        return recipe
    
    @api.marshal_with(recipe_model)
    @jwt_required()
    def put(self,id):
        """update a recipe"""
        data = request.get_json()
        recipe_to_updated = Recipe.query.get_or_404(id)
        recipe_to_updated.update(name=data.get('name'),description=data.get('description'))
        return recipe_to_updated

    @jwt_required()
    def delete(self,id):
        """delete a recipe"""
        recipe_to_deleted = Recipe.query.get_or_404(id)
        recipe_to_deleted.delete()
        return {'success':'Recipe Deleted Successfully'}


@app.shell_context_processor
def make_shell_context():
    return {
        "db":db,
        "Recipe":Recipe,
    }


if __name__ == "__main__":
    app.run()


