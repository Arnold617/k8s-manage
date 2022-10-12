from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .json_response import JsonResponse


class AppPageNumberPagination(PageNumberPagination):
    page_size = 15
    max_page_size = 10
    page_size_query_param = 'size'
    page_query_param = 'page'

    '''
        page_query_param：表示url中的页码参数
		page_size_query_param：表示url中每页数量参数
		page_size：表示每页的默认显示数量
		max_page_size：表示每页最大显示数量，做限制使用，避免突然大量的查询数据，数据库崩溃
    '''

    def get_paginated_response(self, data):
        return JsonResponse(data=data, code=200, msg="success", status=status.HTTP_200_OK, next=self.get_next_link(),
                            previous=self.get_previous_link(), count=self.page.paginator.count)