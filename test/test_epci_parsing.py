# -*- coding: utf-8 -*-

import sys
import unittest2

from unipath import Path
sys.path.append(Path(__file__).ancestor(2))

from scrapy.selector import Selector

from utils import get_response

from localfinance.parsing.zone import EPCIZoneParser


class EPCIFinance2008ParsingTest(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/epci_2008_account.html', encoding='windows-1252')
        self.data = {
            'name': 'GFP : CC MONTAGNE BOURBONNAISE',
            'population': 6858,
            'operating_revenues': 593000,
            'local_tax': 80000,
            'home_tax_basis': 5855000,
            'home_tax_value': 24000,
            'home_tax_rate': 0.0041,
            'property_tax_basis': 4456000,
            'property_tax_value': 22000,
            'property_tax_rate': 0.0050,
            'business_tax_basis': 3172000,
            'business_tax_value': 25000,
            'business_tax_rate': 0.0077,
        }

    def test_parsing(self):
        parser = EPCIZoneParser('', 2008, '', '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class EPCIFinance2010ParsingTest(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/epci_2010_account.html', encoding='windows-1252')
        self.data = {
            'name': 'GFP : CC MONTAGNE BOURBONNAISE',
            'population': 6843,
            'operating_revenues': 606000,
            'compensation_2010_value': 26000,
            'business_property_contribution_additionnal_value': 8000,
            'business_property_contribution_uniq_value': 0,
            'business_property_contribution_eolien_value': 0,
        }

    def test_parsing(self):
        parser = EPCIZoneParser('', 2010, '', '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class EPCIFinance2013ParsingTest(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/epci_2013_account.html', encoding='windows-1252')
        self.data = {
            'name': 'GFP : CC MONTAGNE BOURBONNAISE',
            'population': 6878,
            'operating_revenues': 715000,
            'additionnal_land_property_tax_value': 0,
            'business_property_contribution_additionnal_value': 11000,
            'business_property_contribution_uniq_value': 0,
            'business_property_contribution_eolien_value': 0,
            'business_profit_contribution_value': 4000,
        }

    def test_parsing(self):
        parser = EPCIZoneParser('', 2013, '', '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class EPCIFinance2014ParsingTest(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/epci_2014_account.html', encoding='windows-1252')
        self.data = {
            'name': 'GFP : CC MONTAGNE BOURBONNAISE',
            'population': 6897,
            'operating_revenues': 753000,
            'home_tax_basis': 6975000,
            'home_tax_rate': 0.0112,
            'home_tax_value': 78000,
            'additionnal_land_property_tax_value': 0,
            'business_property_contribution_additionnal_value': 11000,
            'business_property_contribution_uniq_value': 0,
            'business_property_contribution_eolien_value': 0,
            'business_profit_contribution_value': 5000,
            'other_tax': 942000,
            'fiscal_repayment': -860000,
        }

    def test_parsing(self):
        parser = EPCIZoneParser('', 2014, '', '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


if __name__ == '__main__':
    unittest2.main()
