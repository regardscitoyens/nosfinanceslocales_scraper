# -*- coding: utf-8 -*-

import sys

import unittest2
from unipath import Path

sys.path.append(Path(__file__).ancestor(2))

from scrapy.selector import Selector
from utils import get_response
from localfinance.parsing.zone import CityZoneParser


class Commune2000ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/commune_2000_account.html', encoding='windows-1252')
        self.data = {
            'population': 116559,
            'name': 'ORLEANS',
            'operating_revenues': 154756 * 1e3,
            'local_tax': 72981 * 1e3,
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
            'debt_annual_costs': 29564 * 1e3,
            'advances_from_treasury': 0,
            'working_capital': 10927 * 1e3,
        }

    def test_parsing(self):
        parser = CityZoneParser('', 2000, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class Commune2009ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/commune_2009_account.html', encoding='windows-1252')
        self.data = {
            'home_tax_basis': 137402 * 1e3,
            'home_tax_rate': 0.2099,
            'home_tax_value': 28841 * 1e3,
            'home_tax_cuts_on_deliberation': 30475 * 1e3,
            'business_tax_value': 0,
            'business_tax_rate': 0,
        }

    def test_parsing(self):
        parser = CityZoneParser('', 2009, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class Commune2011ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/commune_leognan_2011_account.html', encoding='windows-1252')
        self.data = {
            'home_tax_basis': 10802 * 1e3,
            'home_tax_rate': 0.1976,
            'home_tax_value': 2134 * 1e3,
            'home_tax_cuts_on_deliberation': 3070 * 1e3,
            'property_tax_value': 1539000,
            'property_tax_rate': 0.1753,
            'land_property_tax_value': 273000.,
            'land_property_tax_rate': 1.2127,
        }

    def test_parsing(self):
        parser = CityZoneParser('', 2011, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class Commune2012ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/commune_2012_account.html')
        self.data = {
            'name': 'AILLANT-SUR-MILLERON',
            'population': 394,
            'operating_revenues': 210000.,
            'local_tax': 114000.,
            'other_tax': 22000.,
            'allocation': 62000.,
            'operating_costs': 214000.,
            'staff_costs': 52000.,
            'purchases_and_external_costs': 69000.,
            'financial_costs': 1000.,
            'contingents': 65000.,
            'paid_subsidies': 7000.,
            'net_profit': -4000.,
            'investment_ressources': 91000.,
            'loans': 0,
            'received_subsidies': 43000,
            'fctva': 11000,
            'returned_properties': 0,
            'investments_usage': 98000,
            'facilities_expenses': 45000,
            'debt_repayments': 53000,
            'costs_to_allocate': 0,
            'fixed_assets': 0,
            'residual_financing_capacity': 7000,
            'thirdparty_balance': 0,
            'financing_capacity': 7000,
            'global_profit': -10000,
            'surplus': -4000,
            'self_financing_capacity': -4000,
            'debt_repayment_capacity': -57000,
            'debt_at_end_year': 47000,
            'debt_annual_costs': 53000,
            'working_capital': 79000,
            'home_tax_basis': 562000.,
            'home_tax_cuts_on_deliberation': 0.,
            'property_tax_basis': 345000.,
            'property_tax_cuts_on_deliberation': 0.,
            'land_property_tax_basis': 63000.,
            'land_property_tax_cuts_on_deliberation': 0.,
            'additionnal_land_property_tax_basis': 0.,
            'additionnal_land_property_tax_cuts_on_deliberation': 0.,
            'business_property_contribution_basis': 0.,
            'business_property_contribution_cuts_on_deliberation': 0.,
            'home_tax_value': 47000.,
            'home_tax_rate': 0.0839,
            'property_tax_value': 39000,
            'property_tax_rate': 0.1136,
            'land_property_tax_value': 27000.,
            'land_property_tax_rate': 0.4395,
            'additionnal_land_property_tax_value': 0.,
            'additionnal_land_property_tax_rate': 0.,
            'business_property_contribution_value': 0.,
            'business_property_contribution_rate': 0.,
            'business_profit_contribution_value': 0.,
            'business_profit_contribution_cuts_on_deliberation': 0.,
            'business_network_tax_value': 0.,
            'business_network_tax_cuts_on_deliberation': 0.,
            'retail_land_tax_value': 0.,
            'retail_land_tax_cuts_on_deliberation': 0.,
        }

    def test_parsing(self):
        parser = CityZoneParser('', 2012, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class Commune2013ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/commune_2013_account.html', encoding='windows-1252')
        self.data = {
            'name': 'ORLEANS',
            'population': 117833,
            'operating_revenues': 180447000,
            'local_tax': 77686000,
            'other_tax': 6442000,
            'allocation': 35901000,
            'operating_costs': 165497000,
            'staff_costs': 78539000,
            'purchases_and_external_costs': 33188000,
            'financial_costs': 2373000,
            'contingents': 60000,
            'paid_subsidies': 26377000,
            'net_profit': 14949000,
            'investment_ressources': 79573000,
            'loans': 12336000,
            'received_subsidies': 12429000,
            'fctva': 6484000,
            'returned_properties': 0,
            'investments_usage': 78029000,
            'facilities_expenses': 54568000,
            'debt_repayments': 12232000,
            'costs_to_allocate': 0,
            'fixed_assets': 0,
            'residual_financing_capacity': -1544000,
            'thirdparty_balance': -1000,
            'financing_capacity': -1545000,
            'global_profit': 16494000,
            'surplus': 32501000,
            'self_financing_capacity': 30827000,
            'debt_repayment_capacity': 18595000,
            'debt_at_end_year': 101223000,
            'debt_annual_costs': 14549000,
            'working_capital': 882000,
            'home_tax_basis': 153650000,
            'home_tax_cuts_on_deliberation': 33055000,
            'property_tax_basis': 151051000,
            'property_tax_cuts_on_deliberation': 0.,
            'land_property_tax_basis': 211000,
            'land_property_tax_cuts_on_deliberation': 0.,
            'additionnal_land_property_tax_basis': 0.,
            'additionnal_land_property_tax_cuts_on_deliberation': 0.,
            'business_property_contribution_basis': 0.,
            'business_property_contribution_cuts_on_deliberation': 0.,
            'home_tax_value': 32251000,
            'home_tax_rate': 0.2099,
            'property_tax_value': 45028000,
            'property_tax_rate': 0.2981,
            'land_property_tax_value': 84000,
            'land_property_tax_rate': 0.3960,
            'additionnal_land_property_tax_value': 0.,
            'additionnal_land_property_tax_rate': 0.,
            'business_property_contribution_value': 0.,
            'business_property_contribution_rate': 0.,
           'business_profit_contribution_value': 0.,
            'business_profit_contribution_cuts_on_deliberation': 0.,
            'business_network_tax_value': 0.,
            'business_network_tax_cuts_on_deliberation': 0.,
            'retail_land_tax_value': 0.,
            'retail_land_tax_cuts_on_deliberation': 0.,
        }

    def test_parsing(self):
        parser = CityZoneParser('', 2013, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


class Commune2014ParsingTestCase(unittest2.TestCase):
    def setUp(self):
        self.response = get_response('test/data/commune_2014_account.html', encoding='windows-1252')
        self.data = {
            'name': 'ORLEANS',
            'population': 117988,
            'operating_revenues': 177973000,
            'local_tax': 78960000,
            'other_tax': 6837000,
            'allocation': 34364000,
            'operating_costs': 164278000,
            'staff_costs': 78955000,
            'purchases_and_external_costs': 32426000,
            'financial_costs': 2294000,
            'contingents': 222000,
            'paid_subsidies': 25526000,
            'net_profit': 13695000,
            'investment_ressources': 64543000,
            'loans': 9249000,
            'received_subsidies': 9744000,
            'fctva': 6704000,
            'returned_properties': 0,
            'investments_usage': 59005000,
            'facilities_expenses': 45118000,
            'debt_repayments': 12608000,
            'costs_to_allocate': 0,
            'fixed_assets': 0,
            'residual_financing_capacity': -5537000,
            'thirdparty_balance': 0,
            'financing_capacity': -5537000,
            'global_profit': 19233000,
            'surplus': 32519000,
            'self_financing_capacity': 29644000,
            'debt_repayment_capacity': 17036000,
            'debt_at_end_year': 97863000,
            'debt_annual_costs': 14780000,
            'working_capital': 5198000,
            'home_tax_basis': 154364000,
            'home_tax_cuts_on_deliberation': 33849000,
            'property_tax_basis': 154047000,
            'property_tax_cuts_on_deliberation': 0.,
            'land_property_tax_basis': 206000,
            'land_property_tax_cuts_on_deliberation': 0.,
            'additionnal_land_property_tax_basis': 0.,
            'additionnal_land_property_tax_cuts_on_deliberation': 0.,
            'business_property_contribution_basis': 0.,
            'business_property_contribution_cuts_on_deliberation': 0.,
            'home_tax_value': 32401000,
            'home_tax_rate': 0.2099,
            'property_tax_value': 45922000,
            'property_tax_rate': 0.2981,
            'land_property_tax_value': 82000,
            'land_property_tax_rate': 0.3960,
            'additionnal_land_property_tax_value': 0.,
            'additionnal_land_property_tax_rate': 0.,
            'business_property_contribution_value': 0.,
            'business_property_contribution_rate': 0.,
            'business_profit_contribution_value': 0.,
            'business_profit_contribution_cuts_on_deliberation': 0.,
            'business_network_tax_value': 0.,
            'business_network_tax_cuts_on_deliberation': 0.,
            'retail_land_tax_value': 0.,
            'retail_land_tax_cuts_on_deliberation': 0.,
        }

    def test_parsing(self):
        parser = CityZoneParser('', 2014, '')
        data = parser.parse(Selector(self.response))
        for key, val in self.data.items():
            self.assertAlmostEqual(data[key], val)


if __name__ == '__main__':
    unittest2.main()
