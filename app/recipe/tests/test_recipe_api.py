from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from core.models import Recipe, Ingredient

from recipe.serializers import RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def specific_recipe_url(recipe_id):
    """Return recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_ingredient(recipe, name='Sample ingredient'):
    """Create and return a sample ingredient"""
    return Ingredient.objects.create(recipe=recipe, name=name)


def sample_recipe(**params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Sample recipe',
        'description': 'Sample recipe description'
    }
    defaults.update(params)

    return Recipe.objects.create(**defaults)


class RecipeApiTests(TestCase):

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        recipe1 = sample_recipe(name='Steak pie')
        sample_recipe(name='Pizza')

        sample_ingredient(recipe1)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('name')
        serializer = RecipeDetailSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_recipes_by_name(self):
        """Test returning a list of recipes filtered by name"""
        recipe1 = sample_recipe(name='Pizza Margarita')
        recipe2 = sample_recipe(name='Paella')
        recipe3 = sample_recipe(name='Pizza Carbonara')
        recipe4 = sample_recipe()

        sample_ingredient(recipe1)

        res = self.client.get(RECIPES_URL, {'name': 'Pizz'})

        serializer1 = RecipeDetailSerializer(recipe1)
        serializer2 = RecipeDetailSerializer(recipe2)
        serializer3 = RecipeDetailSerializer(recipe3)
        serializer4 = RecipeDetailSerializer(recipe4)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer3.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertNotIn(serializer4.data, res.data)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail"""
        recipe = sample_recipe()
        sample_ingredient(recipe)

        url = specific_recipe_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe_with_ingredients(self):
        """Test creating recipe"""
        ingredient_name1 = 'cheese'
        ingredient_name2 = 'tomato'
        payload = {
            'name': 'Pizza',
            'description': 'Put it in the oven',
            'ingredients': [
                {'name': ingredient_name1},
                {'name': ingredient_name2}
            ]
        }
        res = self.client.post(
            RECIPES_URL,
            payload,
            content_type="application/json"
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        self.assertEquals(recipe.name, payload['name'])
        self.assertEquals(recipe.description, payload['description'])
        ingredients = recipe.ingredients.all()
        self.assertEquals(ingredients.count(), 2)
        self.assertEquals(ingredients.filter(name=ingredient_name1).count(), 1)
        self.assertEquals(ingredients.filter(name=ingredient_name2).count(), 1)

    def test_update_recipe_with_ingredients(self):
        """Test updating recipe"""
        old_ingredient_name1 = 'cheese'
        old_ingredient_name2 = 'ham'
        new_ingredient_name = 'vegan cheese'
        recipe = sample_recipe(name='Pizza')
        sample_ingredient(recipe, name=old_ingredient_name1)
        sample_ingredient(recipe, name=old_ingredient_name2)
        payload = {
            'name': 'Vegan Pizza',
            'description': 'Put it in the oven 15 min',
            'ingredients': [{'name': new_ingredient_name}]
        }
        url = specific_recipe_url(recipe.id)
        res = self.client.patch(url, payload, content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe = Recipe.objects.get(id=res.data['id'])
        self.assertEquals(recipe.name, payload['name'])
        self.assertEquals(recipe.description, payload['description'])
        ingredients = recipe.ingredients.all()
        self.assertEquals(ingredients.count(), 1)
        self.assertEquals(ingredients.filter(
            name=new_ingredient_name
        ).count(), 1)

    def test_update_recipe_without_ingredients(self):
        """Test updating recipe"""
        new_ingredient_name = 'vegan cheese'
        recipe = sample_recipe(name='Pizza')
        payload = {
            'name': 'Vegan Pizza',
            'description': 'Put it in the oven 15 min',
            'ingredients': [{'name': new_ingredient_name}]
        }
        url = specific_recipe_url(recipe.id)
        res = self.client.patch(url, payload, content_type="application/json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEquals(recipe.name, payload['name'])
        self.assertEquals(recipe.description, payload['description'])
        ingredients = recipe.ingredients.all()
        self.assertEquals(ingredients.count(), 1)
        self.assertEquals(ingredients.filter(
            name=new_ingredient_name
        ).count(), 1)

    def test_delete_recipe(self):
        """Test deleting recipe"""
        recipe = sample_recipe(name='Pizza')
        sample_ingredient(recipe)
        sample_ingredient(recipe)
        recipe2 = sample_recipe()
        remaining_ingredient_name = 'Remaining ingredient'
        sample_ingredient(recipe2, name=remaining_ingredient_name)

        url = specific_recipe_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(id=recipe.id)
        remaining_ingredients = Ingredient.objects.all()
        self.assertEquals(remaining_ingredients.count(), 1)
        self.assertEquals(remaining_ingredients.filter(
            name=remaining_ingredient_name
        ).count(), 1)
