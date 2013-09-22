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

class CommuneParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/commune_2012_account.html')

    def test_parsing(self):
        parser = CityParser('', 2012, '')
        data = parser.parse(self.response)
        self.assertEqual(data['name'], 'AILLANT-SUR-MILLERON')
        self.assertEqual(data['population'], 394)
        # test data parsed from first table
        self.assertEqual(data['operating_revenues'], 210000.)
        self.assertEqual(data['localtax'], 114000.)
        self.assertEqual(data['other_tax'], 22000.)
        self.assertEqual(data['allocation'], 62000.)
        self.assertEqual(data['operating_costs'], 214000.)
        self.assertEqual(data['staff_costs'], 52000.)
        self.assertEqual(data['purchases_and_external_costs'], 69000.)
        self.assertEqual(data['financial_costs'], 1000.)
        self.assertEqual(data['contingents'], 65000.)
        self.assertEqual(data['paid_subsidies'], 7000.)
        self.assertEqual(data['net_profit'], -4000.)
        self.assertEqual(data['investment_ressources'], 91000.)
        self.assertEqual(data['loans'], 0)
        self.assertEqual(data['received_subsidies'], 43000)
        self.assertEqual(data['fctva'], 11000)
        self.assertEqual(data['returned_properties'], 0)
        self.assertEqual(data['investments_usage'], 98000)
        self.assertEqual(data['facilities_expenses'], 45000)
        self.assertEqual(data['debt_repayments'], 53000)
        self.assertEqual(data['costs_to_allocate'], 0)
        self.assertEqual(data['fixed_assets'], 0)
        self.assertEqual(data['residual_financing_capacity'], 7000)
        self.assertEqual(data['thirdparty_balance'], 0)
        self.assertEqual(data['financing_capacity'], 7000)
        self.assertEqual(data['global_profit'], -10000)
        self.assertEqual(data['surplus'], -4000)
        self.assertEqual(data['self_financing_capacity'], -4000)
        self.assertEqual(data['debt_repayment_capacity'], -57000)
        self.assertEqual(data['debt_at_end_year'], 47000)
        self.assertEqual(data['debt_annual_costs'], 53000)
        self.assertEqual(data['working_capital'], 79000)

        # test data parsed from second table
        self.assertEqual(data['home_tax_basis'], 562000.)
        self.assertAlmostEqual(data['home_tax_cuts_on_deliberation'], 0.)
        self.assertEqual(data['property_tax_basis'], 345000.)
        self.assertEqual(data['property_tax_cuts_on_deliberation'], 0.)
        self.assertEqual(data['land_property_tax_basis'], 63000.)
        self.assertEqual(data['land_property_tax_cuts_on_deliberation'], 0.)
        self.assertEqual(data['additionnal_land_property_tax_basis'], 0.)
        self.assertEqual(data['additionnal_land_property_tax_cuts_on_deliberation'], 0.)
        self.assertEqual(data['business_property_contribution_basis'], 0.)
        self.assertEqual(data['business_property_contribution_cuts_on_deliberation'], 0.)
        self.assertEqual(data['home_tax_value'], 47000.)
        self.assertAlmostEqual(data['home_tax_rate'], 0.0839)
        self.assertEqual(data['property_tax_value'], 39000)
        self.assertAlmostEqual(data['property_tax_rate'], 0.1136)
        self.assertEqual(data['land_property_tax_value'], 27000.)
        self.assertAlmostEqual(data['land_property_tax_rate'], 0.4395)
        self.assertEqual(data['additionnal_land_property_tax_value'], 0.)
        self.assertEqual(data['additionnal_land_property_tax_rate'], 0.)
        self.assertEqual(data['business_property_contribution_value'], 0.)
        self.assertEqual(data['business_property_contribution_rate'], 0.)
        self.assertEqual(data['business_profit_contribution_value'], 0.)
        self.assertEqual(data['business_profit_contribution_cuts_on_deliberation'], 0.)
        self.assertEqual(data['business_network_tax_value'], 0.)
        self.assertEqual(data['business_network_tax_cuts_on_deliberation'], 0.)
        self.assertEqual(data['retail_land_tax_value'], 0.)
        self.assertEqual(data['retail_land_tax_cuts_on_deliberation'], 0.)

class Commune2000ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/commune_2000_account.html', encoding='windows-1252')
        self.data = {
            'population': 116559,
            'name': 'ORLEANS',
            'operating_revenues': 154756 * 1e3,
            'localtax': 72981 * 1e3,
            'other_tax': 4549 * 1e3,
            'allocation': 30959 * 1e3,
            'operating_costs': 125548 * 1e3,
            'staff_costs': 58592 * 1e3,
            'purchases_and_external_costs': 27790 * 1e3,
            'financial_costs': 4756 * 1e3,
            'contingents': 1839 * 1e3,
            'paid_subsidies': 23568 * 1e3,
            'net_profit': 29208 * 1e3,
            'home_tax_value': 19394 * 1e3,
            'home_tax_rate': 0.1756,
            'property_tax_value': 25575 * 1e3,
            'property_tax_rate': 0.2440,
            'land_property_tax_value': 66 * 1e3,
            'land_property_tax_rate': 0.3313,
            'business_tax_value': 26711 * 1e3,
            'business_tax_rate': 0.1703,
            'investment_ressources': 118468 * 1e3,
            'loans': 30969 * 1e3,
            'received_subsidies': 7837 * 1e3,
            'fctva': 3014 * 1e3,
            'returned_properties': 0,
            'investments_usage': 125254 * 1e3,
            'facilities_expenses': 50482 * 1e3,
            'debt_repayments': 25686 * 1e3,
            'costs_to_allocate': 2073 * 1e3,
            'fixed_assets': 30466 * 1e3,
            'residual_financing_capacity': 6786 * 1e3,
            'thirdparty_balance': 1000,
            'financing_capacity': 6787 * 1e3,
            'global_profit': 22421 * 1e3,
            'surplus': 24048 * 1e3,
            'self_financing_capacity': 33096 * 1e3,
            'debt_repayment_capacity': 7410 * 1e3,
            'debt_at_end_year': 96199 * 1e3,
            'debt_annual_costs': 29564  * 1e3,
            'advances_from_treasury': 0,
            'working_capital': 10927 * 1e3,
        }

    def test_parsing(self):
        parser = CityParser('', 2000, '')
        data = parser.parse(self.response)
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)

class Commune2009ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/commune_2009_account.html', encoding='windows-1252')
        self.data = {
            'home_tax_basis': 137402 * 1e3,
            'home_tax_rate': 0.2099,
            'home_tax_value': 28841 * 1e3,
            'home_tax_cuts_on_deliberation': 30475 * 1e3,
            'business_tax_value': 0,
            'business_tax_rate': 0,
        }

    def test_parsing(self):
        parser = CityParser('', 2009, '')
        data = parser.parse(self.response)
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)

class EPCIFinanceParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/epci_2012_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = EPCIParser('', 2012, '')
        data = parser.parse(self.response)
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
        parser = EPCIParser('', 2010, '')
        data = parser.parse(self.response)
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
        parser = EPCIParser('', 2008, '')
        data = parser.parse(self.response)
        for key in ['property_tax_basis', 'property_tax_value',
                    'home_tax_value', 'property_tax_rate', 'home_tax_rate',
                    'home_tax_basis', 'business_tax_value', 'business_tax_rate',
                    'business_tax_basis']:
            print key
            self.assertTrue(key in data)

class DepartmentFinanceParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/department_2012_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = DepartmentParser('', 2012, '')
        data = parser.parse(self.response)
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
        parser = DepartmentParser('', 2011, '')
        data = parser.parse(self.response)
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
        parser = DepartmentParser('', 2010, '')
        data = parser.parse(self.response)
        for key in ['tipp', 'property_tax_basis', 'property_tax_value',
                    'compensation_2010_value', 'home_tax_value',
                    'property_tax_rate', 'home_tax_rate']:
            self.assertTrue(key in data)

class DepartmentFinance2009ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/department_2009_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = DepartmentParser('', 2009, '')
        data = parser.parse(self.response)
        for key in ['tipp', 'property_tax_basis', 'property_tax_value',
                    'business_tax_value', 'home_tax_value',
                    'property_tax_rate', 'home_tax_rate']:
            self.assertTrue(key in data)

class DepartmentFinance2008ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/department_2008_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = DepartmentParser('', 2008, '')
        data = parser.parse(self.response)
        for key in ['tipp', 'property_tax_basis', 'property_tax_value',
                    'property_tax_rate', 'home_tax_rate', 'business_tax_rate']:
            self.assertTrue(key in data)

class RegionFinanceParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/region_2012_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = RegionParser('', 2012, '')
        data = parser.parse(self.response)
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
        parser = RegionParser('', 2008, '')
        data = parser.parse(self.response)
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
        parser = RegionParser('', 2009, '')
        data = parser.parse(self.response)
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

if __name__ == '__main__':
    unittest2.main()
