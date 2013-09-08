# -*- coding: utf-8 -*-
from collections import defaultdict

from scrapy.selector import HtmlXPathSelector

from .account_network import city_account


def convert_value(val):
    """Remove crap from val string and then convert it into float"""
    val = val.replace(u'\xa0', '')\
             .replace(',', '.')\
             .replace('-', '')\
             .replace(u'\xa0', '')\
             .replace(' ', '')
    if val:
        if '%' in val:
            val = float(val.replace('%', ''))/100
        return float(val)
    else:
        return None



class CityParser(object):
    """Parser of city html page"""
    zone_type = 'city'
    account = city_account
    def __init__(self, insee_code, year):
        self.data = {'insee_code':insee_code,
                     'year': year,
                     'zone_type': self.zone_type}

        # In the table with financial data, the values we want to scrap are in 
        # the first columns, the name of the data is in the third column.
        self.finance_value_icol = 0
        self.finance_name_icol = 3

        # In the table with tax data, the values can be in the first column and
        # the fourth. The name of the data in third column.
        self.tax_values_icol = [0, 4]
        self.tax_name_icol = 3

    def parse(self, response):
        """Parse html account table of a city for a given year
        crawled from http://alize2.finances.gouv.fr.
        Return a dictionnary which contains scraped data"""
        hxs = HtmlXPathSelector(response)

        data = self.data.copy()
        data['population'] = self.population(hxs)
        data['name'] = self.name(hxs)

        data.update(self.finance(hxs))

        # For years > 2008, we have also tax data
        if int(data['year']) > 2008:
            data.update(self.taxes(hxs))

        return data

    def name(self, hxs):
        return self.table1(hxs).select('.//tr[position()=2]/td[position()=2]/text()').extract()[0]

    def population(self, hxs):
        pop = self.table1(hxs).select('.//tr[position()=3]').re(r': ([\d\s]+) habitants')[0]
        return int(pop.replace(' ', ''))

    def table1(self, hxs):
        """Select table where we have name, population, and finance data"""
        return hxs.select('//body/table[position()=3]')

    def table2(self, hxs):
        """Select table where we have tax data"""
        return hxs.select('//body/table[position()=4]')

    def finance(self, hxs):
        # For this table, we have:
        # - the value is always in the first column of the table. If there is no value,
        # this is just section of the account of the city.
        # - the name of the row is defined the third column.

        data = {}

        for tr in self.table1(hxs).select('.//tr')[4:]:
            tds = tr.select('.//td/text()')
            if len(tds) <= self.finance_name_icol:
                continue
            name = tds[self.finance_name_icol].extract()
            name = name.replace('dont :', '').strip()
            targets = self.account.find_node(name=name, type='accountline')
            if targets:
                target = targets[0]
                value = convert_value(tds[self.finance_value_icol].extract()) * 1000
                if value is not None:
                    data[target] = value
            else:
                print "There is no node of name %s "%name

        return data

    def taxes(self, hxs):
        data = self.basis_taxes(hxs)
        def update_data(new_data):
            for k, v in new_data.items():
                if type(v) == dict:
                    data[k].update(v)
                else:
                    data[k] = v
        update_data(self.tax_cuts_on_deliberation(hxs))
        update_data(self.tax_revenues(hxs))
        update_data(self.tax_rates(hxs))
        update_data(self.repartition_taxes(hxs))
        return data

    def parse_one_tax_info(self, hxs, info_name, icol_value, start_row, end_row, is_percent=False):
        data = defaultdict(dict)
        for row in self.table2(hxs).select('.//tr')[start_row:end_row]:
            tds = row.select('.//td/text()')
            if len(tds) < max(icol_value, self.tax_name_icol):
                continue
            name = tds[self.tax_name_icol].extract().strip()
            targets = self.account.find_node(name=name, type='accountline')
            if targets:
                target = targets[0]
                str_val = tds[icol_value].extract()
                val = convert_value(str_val)
                if not is_percent:
                    val = val * 1000 if val else None
                data[target][info_name] = val
        return data

    def basis_taxes(self, hxs):
        return self.parse_one_tax_info(hxs, 'basis', 0, 4, 9)

    def tax_cuts_on_deliberation(self, hxs):
        return self.parse_one_tax_info(hxs, 'cuts_on_deliberation', 4, 4, 9)

    def tax_revenues(self, hxs):
        return self.parse_one_tax_info(hxs, 'value', 0, 10, 15)

    def tax_rates(self, hxs):
        return self.parse_one_tax_info(hxs, 'rate', 4, 10, 15, is_percent=True)

    def repartition_taxes(self, hxs):
        return self.parse_one_tax_info(hxs, 'value', 0, 18, 21)

class EPCIParser(object):
    zone_type = 'epci'



