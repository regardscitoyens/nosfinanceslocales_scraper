# -*- coding: utf-8 -*-

import sys

import unittest2
from unipath import Path

sys.path.append(Path(__file__).ancestor(2))

from scrapy.selector import Selector

from utils import get_response

from localfinance.parsing.zone import DepartmentZoneParser


class DepartmentFinance2008ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/department_2008_account.html',
                                     encoding='windows-1252')
        self.data = {
            'population': 535489,
            'operating_revenues': 455303000,
            'operating_real_revenues': 453230000,
            'local_tax': 183583000,
            'refund_tax': 0,
            'other_tax': 99211000,
            'advertisement_tax': 34398000,
            'tipp': 31453000,
            'allocation_and_stake': 158788000,
            'allocation': 109209000,
            'realignment': 17887000,
            'operating_costs': 426105000,
            'operating_real_costs': 392785000,
            'staff_costs': 77310000,
            'purchases_and_external_costs': 57394000,
            'subsidies_and_contingents': 247743000,
            'mandatory_contributions_and_stakes': 52527000,
            'subsidies': 17595000,
            'individual_aids': 174671000,
            'pch': 5510000,
            'apa': 40781000,
            'rsa': 0,
            'accomodation_costs': 0,
            'financial_costs': 9761000,
            'net_profit': 29198000,
            'self_financing_capacity': 60444000,
            'investment_ressources': 155286000,
            'fctva': 7913000,
            'received_subsidies': 20379000,
            'sold_fixed_assets': 704000,
            'loans': 45000000,
            'investments_usage': 129789000,
            'investments_direct_costs': 68893000,
            'paid_subsidies': 44227000,
            'debt_repayments': 14897000,
            'residual_financing_capacity': -25497000,
            'thirdparty_balance': 323000,
            'financing_capacity': -25173000,
            'global_profit': 54372000,
            'debt_at_end_year': 260957000,
            'debt_annual_costs': 24298000,
            'home_tax_value': 50719000,
            'home_tax_basis': 441803000,
            'home_tax_rate': 0.1148,
            'home_tax_cuts_on_deliberation': 1146000,
            'property_tax_value': 59808000,
            'property_tax_basis': 385356000,
            'property_tax_rate': 0.1552,
            'property_tax_cuts_on_deliberation': 953000,
            'land_property_tax_value': 587000,
            'land_property_tax_basis': 1745000,
            'land_property_tax_rate': 0.3363,
            'land_property_tax_cuts_on_deliberation': 4000,
            'business_tax_value': 73789000,
            'business_tax_basis': 822619000,
            'business_tax_rate': 0.0897,
            'business_tax_cuts_on_deliberation': 1637000,
        }

    def test_parsing(self):
        parser = DepartmentZoneParser('', 2008, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class DepartmentFinance2009ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/department_2009_account.html', encoding='windows-1252')
        self.data = {
            'population': 537061,
            'operating_revenues': 465068000,
            'operating_real_revenues': 459748000,
            'local_tax': 193093000,
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


class DepartmentFinance2010ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/department_2010_account.html',
                                     encoding='windows-1252')
        self.data = {
            'population':  537820,
            'operating_revenues': 504060000,
            'operating_real_revenues': 498856000,
            'local_tax': 213518000,
            'refund_tax': 0,
            'other_tax': 113116000,
            'advertisement_tax': 30331000,
            'tipp': 45951000,
            'allocation_and_stake': 160322000,
            'compensation_2010_value': 79465000
        }

    def test_parsing(self):
        parser = DepartmentZoneParser('', 2010, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class DepartmentFinance2011ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/department_2011_account.html',
                                     encoding='windows-1252')
        self.data = {
            'property_tax_basis': 430294000,
            'property_tax_value': 136490000,
            'property_tax_rate': 0.3172,
            'business_profit_contribution_basis': 0,
            'business_profit_contribution_value': 38474000,
            'business_network_tax_value': 913000,
        }

    def test_parsing(self):
        parser = DepartmentZoneParser('', 2011, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class DepartmentFinance2012ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/department_2012_account.html',
                                     encoding='windows-1252')
        self.data = {
            'property_tax_basis': 445315000,
            'property_tax_value': 141253000,
            'property_tax_rate': 0.3172,
            'business_profit_contribution_basis': 0,
            'business_profit_contribution_value': 40288000,
            'business_network_tax_value': 974000,
        }

    def test_parsing(self):
        parser = DepartmentZoneParser('', 2012, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class DepartmentFinance2013ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/department_2013_account.html',
                                     encoding='windows-1252')
        self.data = {
            'operating_revenues': 531628000,
            'local_tax': 188257000,
            'other_tax': 140564000,
            'advertisement_tax': 31324000,
            'allocation': 111353000,
            'working_capital': 25320000,
            'property_tax_basis': 458250000,
            'property_tax_value': 145357000,
            'property_tax_rate': 0.3172,
            'business_profit_contribution_basis': 0,
            'business_profit_contribution_value': 40973000,
            'business_network_tax_value': 1004000,
        }

    def test_parsing(self):
        parser = DepartmentZoneParser('', 2013, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


if __name__ == '__main__':
    unittest2.main()
