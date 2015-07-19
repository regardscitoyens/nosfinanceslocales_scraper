# -*- coding: utf-8 -*-

import sys
import unittest2

from unipath import Path
sys.path.append(Path(__file__).ancestor(2))

from scrapy.selector import Selector

from utils import get_response

from localfinance.parsing.zone import RegionZoneParser


class RegionFinance2008ParsingTest(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/region_2008_account.html', encoding='windows-1252')

        self.data = {
            'name': 'REGION BASSE-NORMANDIE',
            'population': 1422193,
            'operating_revenues': 517789000,
            'tipp': 92536000,
            'operating_costs': 411269000,
            'property_tax_basis': 1146012000,
            'property_tax_value': 60623000,
            'property_tax_rate': 0.0529,
            'land_property_tax_basis': 8771000,
            'land_property_tax_value': 631000,
            'land_property_tax_rate': 0.0716,
            'business_tax_basis': 2686771000,
            'business_tax_value': 85439000,
            'business_tax_rate': 0.0318,
        }

    def test_parsing(self):
        parser = RegionZoneParser('', 2008, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class RegionFinance2009ParsingTest(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/region_2009_account.html', encoding='windows-1252')

        self.data = {
            'tipp': 97982000,
            'operating_costs': 445046000,
            'property_tax_basis': 1201584000,
            'property_tax_cuts_on_deliberation': 42000,
            'property_tax_value': 63566000,
            'property_tax_rate': 0.0529,
            'business_tax_basis': 2777345000,
            'business_tax_cuts_on_deliberation': 40309000,
            'business_tax_value': 88318000,
            'business_tax_rate': 0.0318,
        }

    def test_parsing(self):
        parser = RegionZoneParser('', 2009, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class RegionFinance2012ParsingTest(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/region_2012_account.html', encoding='windows-1252')

        self.data = {
            'name': 'REGION BASSE-NORMANDIE',
            'population': 1470880,
            'operating_revenues': 572356000,
            'tipp': 113678000,
            'business_profit_contribution_value': 64681000,
            'business_profit_contribution_cuts_on_deliberation': 288000,
            'business_network_tax_value': 13299000,
        }

    def test_parsing(self):
        parser = RegionZoneParser('', 2012, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class RegionFinance2013ParsingTest(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/region_2013_account.html', encoding='windows-1252')

        self.data = {
            'name': 'REGION BASSE-NORMANDIE',
            'population': 1473494,
            'local_tax': 80964000,
            'operating_revenues': 572776000,
            'tipp': 114518000,
            'business_profit_contribution_value': 66810000,
            'business_profit_contribution_cuts_on_deliberation': 140000,
            'business_network_tax_value': 13616000,
        }

    def test_parsing(self):
        parser = RegionZoneParser('', 2013, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)




if __name__ == '__main__':
    unittest2.main()
