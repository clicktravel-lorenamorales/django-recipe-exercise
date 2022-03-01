from rest_framework import viewsets

from core.models import Recipe

from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Retrieve the recipes"""
        name = self.request.query_params.get('name')
        queryset = self.queryset.order_by('name')

        if name is not None:
            queryset = queryset.filter(name__contains=name)

        return queryset
