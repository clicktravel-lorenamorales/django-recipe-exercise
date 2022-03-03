from django.test import SimpleTestCase

from core import models


class ModelTests(SimpleTestCase):

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe(
            name='Pizza',
            description='Put in the oven'
        )

        self.assertEquals(str(recipe), recipe.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient(
            name='Mozzarela',
            recipe=models.Recipe(
                name='Pizza',
                description='Put in the oven'
            )
        )

        self.assertEquals(str(ingredient), ingredient.name)
