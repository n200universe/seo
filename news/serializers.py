
from rest_framework import serializers
from .models import Category, Post
from django.conf import settings


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'image', 'title','slug', 'content', 'status', 'category', 'published')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'slug', 'title')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields= ('id', 'name', 'slug',)