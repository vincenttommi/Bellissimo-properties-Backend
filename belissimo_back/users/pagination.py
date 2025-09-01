from rest_framework.pagination import PageNumberPagination
from .utils import paginated_custom_response




class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


    def get_paginated_response(self, data):
        return paginated_custom_response(
            paginator = self,
            page  = self.page,
            data = data,
            message = "Data retrieved successfully"
        )