from rest_framework.routers import DefaultRouter
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token


from api.views import CategoryViewSet, ProductViewSet, ShoppingCartViewSet


app_name = "api"

router = DefaultRouter()

router.register("categories", CategoryViewSet, basename="categories")
router.register("products", ProductViewSet, basename="products")
router.register("cart", ShoppingCartViewSet, basename="cart")


urlpatterns = [
    path("", include(router.urls)),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
