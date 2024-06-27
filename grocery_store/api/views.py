import io

from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    SAFE_METHODS,
    AllowAny,
)
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import action

# from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse

# from reportlab.pdfgen import canvas
# from reportlab.pdfbase import pdfmetrics, ttfonts
from django.db.models import Sum
from django.conf import settings

from api.serializers import (
    CategorySerializer,
    SubcategorySerializer,
    ProductSerializer,
    ShoppingCartSerializer,
)
from categories.models import Category, Subcategory, Product
from api.pagination import CategoryPagination


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    pagination_class = CategoryPagination


class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    pagination_class = CategoryPagination


class ShoppingCartViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            pass
