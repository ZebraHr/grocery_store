from rest_framework import serializers

from categories.models import (
    Category,
    Subcategory,
    Product,
    CartProduct,
    ShoppingCart,
)


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегории."""

    class Meta:
        exclude = ("category",)
        model = Subcategory


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории."""

    subcategories = SubcategorySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        fields = ("id", "name", "slug", "image", "subcategories")
        model = Category


class SubcategoryForProdSerializer(serializers.ModelSerializer):
    """Сериализатор для подкатегории при выводе инфорцмации по продукту."""

    class Meta:
        fields = ("name",)
        model = Subcategory


class CategoryForProdSerializer(serializers.ModelSerializer):
    """Сериализатор для категории при выводе инфорцмации по продукту."""

    class Meta:
        fields = ("name",)
        model = Category


class ProductShortSerialiser(serializers.ModelSerializer):
    """Сериализатор для вывода только названия продукта."""

    class Meta:
        fields = ("name",)
        model = Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор по продукту."""

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


class CartProductSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода информации по продукту в корзине."""

    product = ProductShortSerialiser(read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartProduct
        fields = ("id", "product", "amount", "total_price")


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор корзины."""

    cart_products = CartProductSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ("id", "user", "cart_products", "total_amount", "total_price")

    def get_total_amount(self, obj):
        return sum(
            cart_product.amount for cart_product in obj.cart_products.all()
        )

    def get_total_price(self, obj):
        return sum(
            cart_product.total_price
            for cart_product in obj.cart_products.all()
        )
