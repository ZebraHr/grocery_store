from rest_framework.routers import DefaultRouter
from django.urls import include, path

from api.views import CategoryViewSet, ProductViewSet


app_name = "api"

router = DefaultRouter()

router.register("categories", CategoryViewSet, basename="categories")
router.register("products", ProductViewSet, basename="products")

urlpatterns = [
    path('', include(router.urls)),
    # path('', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
]
