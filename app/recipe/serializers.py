from rest_framework import serializers

from core.models import Ingredient, Recipe


class IngredientSerialiser(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingredients = IngredientSerialiser(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'ingredients']
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe_created = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            Ingredient.objects.create(
                name=ingredient['name'],
                recipe=recipe_created
            )
        return recipe_created

    def update(self, instance, validated_data):
        instance.ingredients.all().delete()
        new_ingredients = validated_data.pop('ingredients')
        super().update(validated_data=validated_data, instance=instance)
        for ingredient in new_ingredients:
            Ingredient.objects.create(name=ingredient['name'], recipe=instance)
        return instance
