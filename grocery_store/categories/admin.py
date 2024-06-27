# from import_export.admin import ImportExportActionModelAdmin
from django.contrib import admin
from django.contrib.admin import display

from categories.models import Category, Subcategory, Product, ShoppingCart


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "image")
    list_filter = ("name",)


@admin.register(Subcategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "image")
    list_filter = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "subcategory", "price")
    list_filter = ("name",)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product")
    list_filter = ("product",)