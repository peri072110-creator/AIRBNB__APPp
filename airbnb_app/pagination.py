from rest_framework.pagination import PageNumberPagination
class PropertyPageNumberPagination(PageNumberPagination):
    page_size = 2

class ReviewPageNumberPagination(PageNumberPagination):
    page_size = 4

