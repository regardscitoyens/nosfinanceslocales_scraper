# -*- coding: utf-8 -*-

import sys
import unittest2

from unipath import Path
sys.path.append(Path(__file__).ancestor(2))

from scrapy.selector import HtmlXPathSelector
from scrapy.http.response.html import HtmlResponse

from localgouv.account_network import parse_page_account

class CommuneFinanceParsingTestCase(unittest2.TestCase):
    def setUp(self):
        body = open('data/test_commune_body.html', 'r').read()
        self.response = HtmlResponse('test', encoding='utf-8')
        self.response.body = body

    def test_parsing(self):
        account = parse_page_account("XXXXX", "XX", 2013, self.response)

        # test data parsed from first table
        self.assertEqual(account.nodes['operating_revenues']['value'], 210000.)
        self.assertEqual(account.nodes['localtax']['value_per_person'], 289.)
        self.assertEqual(account.nodes['operating_costs']['value_per_person'], 542.)

        # test data parsed from second table
        self.assertEqual(account.nodes['home_tax']['value'], 47000.)
        self.assertEqual(account.nodes['home_tax']['basis'], 562000.)
        self.assertEqual(account.nodes['home_tax']['voted_rate'], 0.0839)

if __name__ == '__main__':
    unittest2.main()
