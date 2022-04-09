from flask_restx import Namespace, Resource, fields
from flask import request
from models import Recipe
from flask_jwt_extended import jwt_required


recipe_ns = Namespace('Recipe',description='A namespace for Recipes')


# model serializer
recipe_model = recipe_ns.model('Recipe',{
    "id":fields.Integer(),
    "name":fields.String(),
    "description":fields.String()
})


@recipe_ns.route('/recipes')
class RecipeResource(Resource):
    @recipe_ns.marshal_list_with(recipe_model)
    @jwt_required()
    def get(self):
        """Get all recipes"""
        recipes = Recipe.query.all()
        return recipes

    @recipe_ns.marshal_with(recipe_model)
    @recipe_ns.expect(recipe_model)
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

@recipe_ns.route('/recipe/<int:id>')
class RecipeResource(Resource):
    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def get(self,id):
        """Get a particular Recipe"""
        recipe = Recipe.query.filter_by(id=id).first()
        return recipe
    
    @recipe_ns.marshal_with(recipe_model)
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