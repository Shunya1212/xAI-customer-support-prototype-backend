from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'total': self.page.paginator.count,
            'pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })
    
    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'links': {
                    'type': 'object',
                    'properties': {
                        'next': {
                            'type': 'string',
                            'nullable': True,
                            'format': 'uri',
                            'example': f'http://api.example.org/accounts/?{self.page_query_param}=4'
                        },
                        'previous': {
                            'type': 'string',
                            'nullable': True,
                            'format': 'uri',
                            'example': f'http://api.example.org/accounts/?{self.page_query_param}=2'
                        },
                    }
                },
                'total': {'type': 'integer', 'example': 1234},
                'pages': {'type': 'integer', 'example': 5},
                'current_page': {'type': 'integer', 'example': 3},
                'results': schema
            }
        }


class LargeResultPagination(StandardResultsSetPagination):
    page_size = 500