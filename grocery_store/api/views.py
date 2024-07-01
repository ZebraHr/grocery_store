from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (
    CategorySerializer,
    ProductSerializer,
    ShoppingCartSerializer,
    CartProductSerializer,
)
from categories.models import Category, Product, ShoppingCart, CartProduct


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для просмотра категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для просмотра продуктов."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """Вьюсет корзины.
       Создание, просмотр, редактирование, очистка."""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def add_product(self, request, pk=None):
        """Создание корзины, если нет.
           Добавление продукта в корзину."""
        user = request.user
        product_id = request.data.get("product_id")
        amount = request.data.get("amount", 1)
        try:
            amount = int(amount)
        except ValueError:
            return Response(
                {"error": "Amount must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cart, created = ShoppingCart.objects.get_or_create(user=user)
        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart, product=product
        )
        if not created:
            cart_product.amount += amount
        else:
            cart_product.amount = amount
        cart_product.save()
        return Response(
            {
                "message": f"Product {product_id} with amount {amount} "
                           f"was added to cart for user {user.id}"
            },
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"])
    def update_product(self, request):
        """Изменение количества продукта в корзине."""
        user = request.user
        product_id = request.data.get("product_id")
        amount = request.data.get("amount")

        try:
            cart = ShoppingCart.objects.get(user=user)
            cart_product = CartProduct.objects.get(
                cart=cart, product__id=product_id
            )
            cart_product.amount = int(amount)
            cart_product.save()

            return Response(
                {
                    "message": f"Amount of product {product_id} in cart was changed to {amount}",
                    "data": CartProductSerializer(cart_product).data,
                },
                status=status.HTTP_200_OK,
            )
        except ShoppingCart.DoesNotExist:
            return Response(
                {"error": "Shopping cart does not exist for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except CartProduct.DoesNotExist:
            return Response(
                {"error": f"Product {product_id} is not in the cart."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["post"])
    def remove_product(self, request):
        """Удаление продукта из корзины."""
        user = request.user
        product_id = request.data.get("product_id")

        try:
            cart = ShoppingCart.objects.get(user=user)
            cart_product = CartProduct.objects.get(
                cart=cart, product__id=product_id
            )
            cart_product.delete()

            return Response(
                {"message": f"Product {product_id} was removed from cart"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except ShoppingCart.DoesNotExist:
            return Response(
                {"error": "Shopping cart does not exist for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except CartProduct.DoesNotExist:
            return Response(
                {"error": f"Product {product_id} is not in the cart."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["post"])
    def clear_cart(self, request):
        """Полная очистка корзины."""
        user = request.user
        try:
            cart = ShoppingCart.objects.get(user=user)
            cart.cart_products.all().delete()
        except ShoppingCart.DoesNotExist:
            return Response(
                {"error": "Shopping cart does not exist for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"message": f"Cart for user {user.id} is now clear."},
            status=status.HTTP_204_NO_CONTENT,
        )
