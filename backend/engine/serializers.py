from rest_framework import serializers
from .models import Tag, Picture

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('tag',)
