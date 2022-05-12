from rest_framework.pagination import PageNumberPagination


class CustomPaginationClass(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'