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
        self.assertEqual(data['contigents'], 65000.)
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
        self.assertEqual(data['business_network_tax_value'], 0.)
        self.assertEqual(data['retail_land_tax_value'], 0.)

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
        self.assertEqual(data['home_tax_value'], 199000.)
        self.assertEqual(data['home_tax_basis'], 8489000.)
        self.assertAlmostEqual(data['home_tax_rate'], 0.023400)
        self.assertEqual(data['home_tax_cuts_on_deliberation'], 33000)

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
        self.assertEqual(data['property_tax_basis'], 129386000)
        self.assertEqual(data['property_tax_value'], 30483000)
        self.assertAlmostEqual(data['property_tax_rate'], 0.2356)
        self.assertEqual(data['business_profit_contribution_cuts_on_deliberation'], 4000)

class RegionFinanceParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('data/region_2012_account.html',
                                     encoding='windows-1252')

    def test_parsing(self):
        parser = RegionParser('', 2012)
        data = parser.parse(self.response)
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

if __name__ == '__main__':
    unittest2.main()
