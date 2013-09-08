# -*- coding: utf-8 -*-

import sys
import unittest2

from unipath import Path
sys.path.append(Path(__file__).ancestor(2))

from scrapy.selector import HtmlXPathSelector
from scrapy.http.response.html import HtmlResponse

from localgouv.account_network import city_account
from localgouv.account_parsing import parse_city_page_account


def get_reponse(filepath):
    body = open(filepath, 'r').read()
    response = HtmlResponse('test', encoding='utf-8')
    response.body = body
    return response

class CommuneFinanceParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/commune_2012_account.html')

    def test_parsing(self):
        data = parse_city_page_account("", "", "2012", self.response)
        # test data parsed from first table
        self.assertEqual(data['operating_revenues'], 210000.)
        self.assertEqual(data['localtax'], 289.)
        self.assertEqual(data['operating_costs'], 542.)

        # test data parsed from second table
        self.assertEqual(data['home_tax']['value'], 47000.)
        self.assertEqual(data['home_tax']['basis'], 562000.)
        self.assertEqual(data['home_tax']['voted_rate'], 0.0839)

if __name__ == '__main__':
    unittest2.main()
