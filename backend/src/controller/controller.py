# Controls the flow of the whole of the back-end
from backend.src.controller import recipe, utils
import json
import os
from controller import recipe


class Controller:
    def __init__(self):
        self.current_recipe = None

    def new_recipe(self, recipe_id):
        self.current_recipe = recipe.Recipe(recipe_id)

    def get_command_for_step(self, step_number):
        return self.current_recipe.get_command_for_step(step_number)

    def get_command_for_current_step(self):
        return self.current_recipe.get_command_for_current_step()

    def get_progression_requirements_for_step(self, step_number):
        return self.current_recipe.get_progression_requirements_for_step(step_number)

    def get_progression_requirements_for_current_step(self):
        return self.current_recipe.get_progression_requirements_for_current_step()

    def get_recipe_metadata(self):
        return self.current_recipe.get_recipe_metadata()

    def get_all_recipe_metadata(self):
        recipes = utils.get_json(utils.get_database_address("Recipes")).get('recipes', [])
        all_metadata = [
                        {'image': recipe.get('image', ''),
                         'name': recipe.get('name', ''),
                         'description': recipe.get('description', '')
                         } for recipe in recipes
                        ]
        return all_metadata


CONTROLLER_INSTANCE = Controller()
