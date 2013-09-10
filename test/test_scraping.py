# -*- coding: utf-8 -*-

import sys
import unittest2

from unipath import Path
sys.path.append(Path(__file__).ancestor(2))

from scrapy.selector import HtmlXPathSelector
from scrapy.http.response.html import HtmlResponse

from localgouv.account_parsing import (
    CityParser,
    EPCIParser,
    DepartmentParser,
    RegionParser
)

def get_response(filepath, encoding='utf-8'):
    body = open(filepath, 'r').read()
    response = HtmlResponse('test', encoding=encoding)
    response.body = body
    return response

class CommuneFinanceParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/commune_2012_account.html')

    def test_parsing(self):
        parser = CityParser('', 2012)
        data = parser.parse(self.response)
        self.assertEqual(data['population'], 394)
        # test data parsed from first table
        self.assertEqual(data['operating_revenues'], 210000.)
        self.assertEqual(data['localtax'], 114000.)
        self.assertEqual(data['operating_costs'], 214000.)

        # test data parsed from second table
        self.assertEqual(data['home_tax']['value'], 47000.)
        self.assertEqual(data['home_tax']['basis'], 562000.)
        self.assertAlmostEqual(data['home_tax']['rate'], 0.0839)

class EPCIFinanceParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/epci_2012_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = EPCIParser('', 2012)
        data = parser.parse(self.response)
        self.assertEqual(data['population'], 2701)
        # test data parsed from first table
        self.assertEqual(data['operating_revenues'], 1879000.)
        self.assertEqual(data['localtax'], 395000.)
        self.assertEqual(data['operating_costs'], 1742000.)

        # test data parsed from second table
        self.assertEqual(data['home_tax']['value'], 199000.)
        self.assertEqual(data['home_tax']['basis'], 8489000.)
        self.assertAlmostEqual(data['home_tax']['rate'], 0.023400)
        self.assertEqual(data['home_tax']['cuts_on_deliberation'], 33000)

class DepartmentFinanceParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/department_2012_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = DepartmentParser('', 2012)
        data = parser.parse(self.response)
        self.assertEqual(data['name'], 'CANTAL')
        self.assertEqual(data['population'], 148380)
        # test data parsed from first table
        self.assertEqual(data['operating_revenues'], 199333000)
        self.assertEqual(data['direct_tax'], 41983000)
        self.assertEqual(data['tipp'], 10860000)
        self.assertEqual(data['operating_costs'], 185946000.)

        # test data parsed from second table
        self.assertEqual(data['property_tax']['basis'], 129386000)
        self.assertEqual(data['property_tax']['value'], 30483000)
        self.assertAlmostEqual(data['property_tax']['rate'], 0.2356)
        self.assertEqual(data['business_profit_contribution']['cuts_on_deliberation'], 4000)

class RegionFinanceParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/region_2012_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = RegionParser('', 2012)
        data = parser.parse(self.response)
        self.assertEqual(data['name'], 'BASSE-NORMANDIE')
        self.assertEqual(data['population'], 1470880)
        # test data parsed from first table
        self.assertEqual(data['operating_revenues'], 572356000)
        self.assertEqual(data['direct_tax'], 78478000)
        self.assertEqual(data['tipp'], 113678000.)
        self.assertEqual(data['operating_costs'], 502385000)

        # test data parsed from second table
        self.assertEqual(data['business_profit_contribution']['value'], 64681000)
        self.assertEqual(data['business_profit_contribution']['cuts_on_deliberation'], 288000)


if __name__ == '__main__':
    unittest2.main()
