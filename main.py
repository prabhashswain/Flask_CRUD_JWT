from flask import Flask,request
from flask_restx import Api,Resource,fields
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

# model serializer
recipe_model = api.model('Recipe',{
    "id":fields.Integer(),
    "name":fields.String(),
    "description":fields.String()
})

@api.route('/recipes')
class RecipeResource(Resource):
    @api.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes"""
        recipes = Recipe.query.all()
        return recipes

    @api.marshal_with(recipe_model)
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
    def get(self,id):
        """Get a particular Recipe"""
        recipe = Recipe.query.filter_by(id=id).first()
        return recipe
    
    @api.marshal_with(recipe_model)
    def put(self,id):
        """update a recipe"""
        data = request.get_json()
        recipe_to_updated = Recipe.query.get_or_404(id)
        recipe_to_updated.update(name=data.get('name'),description=data.get('description'))
        return recipe_to_updated


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


