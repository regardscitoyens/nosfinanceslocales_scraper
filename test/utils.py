# -*- coding: utf-8 -*-

from scrapy.http.response.html import HtmlResponse


def get_response(filepath, encoding='utf-8'):
    body = open(filepath, 'r').read()
    response = HtmlResponse('test', encoding=encoding, body=body)
    return response
