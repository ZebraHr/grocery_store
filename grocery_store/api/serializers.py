# import base64

# import webcolors
# from dataclasses import fields
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.conf import settings

from categories.models import Category, Subcategory, Product


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ("category",)
        model = Subcategory


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        fields = ("id", "name", "slug", "image", "subcategories")
        model = Category


class SubcategoryForProdSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name",)
        model = Subcategory


class CategoryForProdSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name",)
        model = Category


class ProductSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.SerializerMethodField()
    image_medium = serializers.SerializerMethodField()
    image_large = serializers.SerializerMethodField()
    category = CategoryForProdSerializer(read_only=True)
    subcategory = SubcategoryForProdSerializer(
        read_only=True,
    )

    class Meta:
        fields = (
            "id",
            "name",
            "slug",
            "category",
            "subcategory",
            "price",
            "image_thumbnail",
            "image_medium",
            "image_large",
        )
        model = Product

    def get_image_thumbnail(self, obj):
        return obj.image_thumbnail.url if obj.image_thumbnail else None

    def get_image_medium(self, obj):
        return obj.image_medium.url if obj.image_medium else None

    def get_image_large(self, obj):
        return obj.image_large.url if obj.image_large else None


class ShoppingCartReadSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления в корзину."""

    pass


class ShoppingCartCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и редактирования корзины."""

    pass
