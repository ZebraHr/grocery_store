from django.contrib import admin
from django.utils.html import format_html

from categories.models import Category, Subcategory, Product


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
    list_display = (
        "id",
        "name",
        "slug",
        "subcategory",
        "price",
        "admin_thumbnail",
    )
    list_filter = ("name",)

    def admin_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px;" />',
                obj.image.url,
            )
        return "No Image"

    admin_thumbnail.short_description = "Thumbnail"
