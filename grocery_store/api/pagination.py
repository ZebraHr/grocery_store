from rest_framework.pagination import PageNumberPagination


class CategoryPagination(PageNumberPagination):
    """Паджинация рецептов."""

    page_size = 6
    page_size_query_param = "limit"
