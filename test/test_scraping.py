# -*- coding: utf-8 -*-

import sys
import unittest2

from unipath import Path
sys.path.append(Path(__file__).ancestor(2))

from scrapy.selector import Selector

from .utils import get_response

from localfinance.parsing.zone import (
    EPCIZoneParser,
    DepartmentZoneParser,
    RegionZoneParser
)


class EPCIFinanceParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/epci_2012_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = EPCIZoneParser('', 2012, '')
        data = parser.parse(Selector(self.response))
        self.assertEqual(data['population'], 2701)
        # test data parsed from first table
        self.assertEqual(data['operating_revenues'], 1879000.)
        self.assertEqual(data['localtax'], 395000.)
        self.assertEqual(data['operating_costs'], 1742000.)

        # test data parsed from second table
        self.assertEqual(data['home_tax_value'], 199000.)
        self.assertEqual(data['home_tax_basis'], 8489000.)
        self.assertAlmostEqual(data['home_tax_rate'], 0.023400)
        self.assertEqual(data['home_tax_cuts_on_deliberation'], 33000)

        for key in ['property_tax_basis', 'property_tax_value',
                    'home_tax_value', 'property_tax_rate', 'home_tax_rate',
                    'business_property_contribution_basis',
                    'business_property_contribution_cuts_on_deliberation']:
            self.assertTrue(key in data)


class EPCIFinance2010ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/epci_2010_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = EPCIZoneParser('', 2010, '')
        data = parser.parse(Selector(self.response))
        for key in ['property_tax_basis', 'property_tax_value',
                    'home_tax_value', 'property_tax_rate', 'home_tax_rate',
                    'home_tax_cuts_on_deliberation', 'home_tax_basis',
                    'business_property_contribution_basis',
                    'business_property_contribution_cuts_on_deliberation'
                    ]:
            self.assertTrue(key in data)

class EPCIFinance2008ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/epci_2008_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = EPCIZoneParser('', 2008, '')
        data = parser.parse(Selector(self.response))
        for key in ['property_tax_basis', 'property_tax_value',
                    'home_tax_value', 'property_tax_rate', 'home_tax_rate',
                    'home_tax_basis', 'business_tax_value', 'business_tax_rate',
                    'business_tax_basis']:
            self.assertTrue(key in data)

class DepartmentFinanceParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/department_2012_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = DepartmentZoneParser('', 2012, '')
        data = parser.parse(Selector(self.response))
        self.assertEqual(data['allocation'], 52327 * 1e3)
        self.assertEqual(data['name'], 'CANTAL')
        self.assertEqual(data['population'], 148380)
        # test data parsed from first table
        self.assertEqual(data['operating_revenues'], 199333000)
        self.assertEqual(data['direct_tax'], 41983000)
        self.assertEqual(data['tipp'], 10860000)
        self.assertEqual(data['operating_costs'], 185946000.)

        # test data parsed from second table
        self.assertEqual(data['property_tax_basis'], 129386000)
        self.assertEqual(data['property_tax_value'], 30483000)
        self.assertAlmostEqual(data['property_tax_rate'], 0.2356)

class DepartmentFinance2011ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/department_2011_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = DepartmentZoneParser('', 2011, '')
        data = parser.parse(Selector(self.response))
        for key in ['tipp', 'property_tax_basis', 'property_tax_value',
                    'property_tax_cuts_on_deliberation', 'property_tax_rate',
                    'business_profit_contribution_basis',
                    'business_network_tax_value']:
            self.assertTrue(key in data)

class DepartmentFinance2010ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/department_2010_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = DepartmentZoneParser('', 2010, '')
        data = parser.parse(Selector(self.response))
        for key in ['tipp', 'property_tax_basis', 'property_tax_value',
                    'compensation_2010_value', 'home_tax_value',
                    'property_tax_rate', 'home_tax_rate']:
            self.assertTrue(key in data)

class DepartmentFinance2009ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/department_2009_account.html', encoding='windows-1252')
        self.data = {
            'population': 537061,
            'operating_revenues': 465068000,
            'operating_real_revenues': 459748000,
            'localtax': 193093000,
            'refund_tax': 0,
            'other_tax': 99257000,
            'tipp': 39185000,
            'allocation_and_stake': 158439000,
            'allocation': 110390000,
            'realignment': 15679000,
            'operating_costs': 463765000,
            'operating_real_costs': 428409000,
            'staff_costs': 86827000,
            'purchases_and_external_costs': 57954000,
            'subsidies_and_contingents': 272400000,
            'mandatory_contributions_and_stakes': 54939000,
            'subsidies': 16009000,
            'individual_aids': 113380000,
            'pch': 7565000,
            'apa': 45375000,
            'rsa': 28671000,
            'accomodation_costs': 79145000,
            'financial_costs': 10238000,
            'net_profit': 1303000,
            'self_financing_capacity': 31339000,
            'debt_at_end_year': 294726000,
            'debt_annual_costs': 26249000,
            'home_tax_value': 52485000,
            'home_tax_basis': 457175000,
            'home_tax_rate': 0.1148,
            'home_tax_cuts_on_deliberation': 0,
            'property_tax_value': 62591000,
            'property_tax_basis': 403301000,
            'property_tax_rate': 0.1552,
            'property_tax_cuts_on_deliberation': 33000,
            'land_property_tax_value': 596000,
            'land_property_tax_basis': 1775000,
            'land_property_tax_rate': 0.3363,
            'land_property_tax_cuts_on_deliberation': 0,
            'business_tax_value': 75344000,
            'business_tax_basis': 839954000,
            'business_tax_rate': 0.0897,
            'business_tax_cuts_on_deliberation': 3937000,
        }

    def test_parsing(self):
        parser = DepartmentZoneParser('', 2009, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class DepartmentFinance2008ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/department_2008_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = DepartmentZoneParser('', 2008, '')
        data = parser.parse(Selector(self.response))
        for key in ['tipp', 'property_tax_basis', 'property_tax_value',
                    'property_tax_rate', 'home_tax_rate', 'business_tax_rate']:
            self.assertTrue(key in data)


class RegionFinanceParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/region_2012_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = RegionZoneParser('', 2012, '')
        data = parser.parse(Selector(self.response))
        self.assertTrue('allocation' in data)
        self.assertEqual(data['name'], 'REGION BASSE-NORMANDIE')
        self.assertEqual(data['population'], 1470880)
        # test data parsed from first table
        self.assertEqual(data['operating_revenues'], 572356000)
        self.assertEqual(data['direct_tax'], 78478000)
        self.assertEqual(data['tipp'], 113678000.)
        self.assertEqual(data['operating_costs'], 502385000)

        # test data parsed from second table
        self.assertEqual(data['business_profit_contribution_value'], 64681000)
        self.assertEqual(data['business_profit_contribution_cuts_on_deliberation'], 288000)


class RegionFinance2008ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/region_2008_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = RegionZoneParser('', 2008, '')
        data = parser.parse(Selector(self.response))
        self.assertTrue('allocation' in data)
        self.assertEqual(data['name'], 'REGION BASSE-NORMANDIE')
        self.assertEqual(data['population'],  1422193)
        # test data parsed from first table
        self.assertEqual(data['operating_revenues'], 517789 * 1e3)
        self.assertEqual(data['direct_tax'], 139801 * 1e3)
        self.assertEqual(data['tipp'], 92536 * 1e3)
        self.assertEqual(data['operating_costs'], 411269 * 1e3)

        # test data parsed from second table
        self.assertEqual(data['property_tax_basis'], 1146012 * 1e3)
        self.assertEqual(data['property_tax_value'], 60623 * 1e3)
        self.assertEqual(data['property_tax_rate'], 0.0529)
        self.assertEqual(data['business_tax_basis'], 2686771 * 1e3)
        self.assertEqual(data['business_tax_value'], 85439 * 1e3)
        self.assertEqual(data['business_tax_rate'], 0.0318)


class RegionFinance2009ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/region_2009_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = RegionZoneParser('', 2009, '')
        data = parser.parse(Selector(self.response))
        self.assertTrue('allocation' in data)
        # test data parsed from first table
        self.assertEqual(data['tipp'], 97982 * 1e3)

        # test data parsed from second table
        self.assertEqual(data['property_tax_basis'], 1201584 * 1e3)
        self.assertEqual(data['property_tax_cuts_on_deliberation'], 42 * 1e3)
        self.assertEqual(data['property_tax_value'], 63566 * 1e3)
        self.assertEqual(data['property_tax_rate'], 0.0529)
        self.assertEqual(data['business_tax_basis'], 2777345 * 1e3)
        self.assertEqual(data['business_tax_cuts_on_deliberation'], 40309 * 1e3)
        self.assertEqual(data['business_tax_value'], 88318 * 1e3)
        self.assertEqual(data['business_tax_rate'], 0.0318)


class RegionFinance2013ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/region_2013_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = RegionZoneParser('', 2013, '')
        data = parser.parse(Selector(self.response))

        print data

        self.assertTrue('allocation' in data)

        self.assertEqual(data['population'], 309693)

        # test data parsed from first table
        self.assertEqual(data['tipp'], 97982 * 1e3)

        # test data parsed from second table
        self.assertEqual(data['property_tax_basis'], 1201584 * 1e3)
        self.assertEqual(data['property_tax_cuts_on_deliberation'], 42 * 1e3)
        self.assertEqual(data['property_tax_value'], 63566 * 1e3)
        self.assertEqual(data['property_tax_rate'], 0.0529)
        self.assertEqual(data['business_tax_basis'], 2777345 * 1e3)
        self.assertEqual(data['business_tax_cuts_on_deliberation'], 40309 * 1e3)
        self.assertEqual(data['business_tax_value'], 88318 * 1e3)
        self.assertEqual(data['business_tax_rate'], 0.0318)


if __name__ == '__main__':
    unittest2.main()
