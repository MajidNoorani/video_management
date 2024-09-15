import math
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        # Calculate total number of pages
        total_pages = math.ceil(self.page.paginator.count / self.page_size)
        return Response({
            'total_pages': total_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'current_page_number': int(self.get_page_number(
                self.request,
                self.page.paginator)),
            'results': data
        })
