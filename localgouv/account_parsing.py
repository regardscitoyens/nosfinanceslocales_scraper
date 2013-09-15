# -*- coding: utf-8 -*-
from collections import defaultdict

from scrapy.selector import HtmlXPathSelector

from .account_network import (
    city_account,
    epci_account,
    department_account,
    region_account
)


def convert_value(val):
    """Remove crap from val string and then convert it into float"""
    val = val.replace(u'\xa0', '')\
             .replace(',', '.')\
             .replace(u'\xa0', '')\
             .replace(' ', '')
    mult = 1

    if '-' in val and len(val) > 1:
        mult = -1
        val = val.replace('-', '')
    elif '-' in val:
        val = '0'

    if val is not None:
        if '%' in val:
            val = float(val.replace('%', ''))/100
        return float(val) * mult
    else:
        print "none"
        return None



class CityParser(object):
    """Parser of city html page"""
    zone_type = 'city'
    account = city_account

    table1_ix = 3
    table2_ix = 4

    # In the table with financial data, the values we want to scrap are in 
    # the first columns, the name of the data is in the third column.
    finance_value_icol = 0
    finance_name_icol = 3

    # In the table with tax data, the values can be in the first column and
    # the fourth. The name of the data in third column.
    tax_values_icol = [0, 4]
    tax_name_icol = 3
    def __init__(self, insee_code, year, url):
        self.data = {'insee_code':insee_code,
                     'year': year,
                     'zone_type': self.zone_type,
                     'url': url}

    def has_taxes(self):
        # For years > 2008, we have also tax data
        return int(self.data['year']) > 2008

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
        if self.has_taxes():
            data.update(self.taxes(hxs))

        return data

    def name(self, hxs):
        return self.table1(hxs).select('.//tr[position()=2]/td[position()=2]/text()').extract()[0]

    def population(self, hxs):
        pop = self.table1(hxs).select('.//tr[position()=3]').re(r': ([\d\s]+) habitants')[0]
        return int(pop.replace(' ', ''))

    def table1(self, hxs):
        """Select table where we have name, population, and finance data"""
        return hxs.select('//body/table[position()=%s]'%self.table1_ix)

    def table2(self, hxs):
        """Select table where we have tax data"""
        return hxs.select('//body/table[position()=%s]'%self.table2_ix)

    def finance(self, hxs):
        # For this table, we have:
        # - the value is always in the first column of the table. If there is no value,
        # this is just section of the account of the city.
        # - the name of the row is defined the third column.

        data = {}

        for tr in self.table1(hxs).select('.//tr')[2:]:
            tds = tr.select('.//td')
            if len(tds) <= self.finance_name_icol:
                continue

            name_td = tds[self.finance_name_icol].select('.//text()').extract()
            if not name_td or not name_td[0].strip():
                ths = tr.select('.//th')
                if ths:
                    name_td = ths[0].select('.//text()').extract()
                    if not name_td:
                        continue
                else:
                    continue
            name = name_td[0]
            name = name.replace('dont', '').replace(':', '').replace('+', '').strip()
            targets = self.account.find_node(name=name, type='accountline')
            if targets:
                target = targets[0]
                try:
                    value = convert_value(tds[self.finance_value_icol]\
                        .select('.//text()').extract()[0]) * 1000
                    if value is not None:
                        data[target] = value
                except IndexError:
                    print "no value for node %s "%name
            else:
                print "There is no node of name %s "%name

        return data

    def taxes(self, hxs):
        data = self.tax_basis(hxs)
        data.update(self.tax_cuts_on_deliberation(hxs))
        data.update(self.tax_revenues(hxs))
        data.update(self.tax_rates(hxs))
        data.update(self.repartition_taxes(hxs))
        return data

    def parse_one_tax_info(self, hxs, info_name, icol_value, start_row, end_row, is_percent=False):
        data = {}
        for row in self.table2(hxs).select('.//tr')[start_row:end_row]:
            tds = row.select('.//td')
            if len(tds) <= max(icol_value, self.tax_name_icol):
                continue
            name = tds[self.tax_name_icol].select('./text()').extract()[0].strip()
            targets = self.account.find_node(name=name, type='accountline')
            if targets:
                target = targets[0]
                str_val = tds[icol_value].select('./text()').extract()[0].strip()
                try:
                    val = convert_value(str_val)
                except ValueError:
                    print u"There is no valid value for the node %s"%target
                    continue

                if not is_percent:
                    val = val * 1000 if val is not None else None
                if info_name:
                    key = "%s_%s"%(target,info_name)
                else:
                    key = target
                data[key] = val
            else:
                print "There is no node of name %s "%name
        return data

    def tax_basis(self, hxs):
        return self.parse_one_tax_info(hxs, 'basis', self.tax_values_icol[0], 4, 9)

    def tax_cuts_on_deliberation(self, hxs):
        return self.parse_one_tax_info(hxs, 'cuts_on_deliberation', self.tax_values_icol[1], 4, 9)

    def tax_revenues(self, hxs):
        return self.parse_one_tax_info(hxs, 'value', self.tax_values_icol[0], 11, 16)

    def tax_rates(self, hxs):
        return self.parse_one_tax_info(hxs, 'rate', self.tax_values_icol[1], 11, 16, is_percent=True)

    def repartition_taxes(self, hxs):
        data = self.parse_one_tax_info(hxs, 'cuts_on_deliberation', self.tax_values_icol[1], 18, 21)
        data.update(self.parse_one_tax_info(hxs, 'value', self.tax_values_icol[0], 18, 21))
        return data
class EPCIParser(CityParser):
    zone_type = 'epci'
    account = epci_account

    # In the table with financial data, the values we want to scrap are in 
    # the first columns, the name of the data is in the third column.
    finance_value_icol = 0
    finance_name_icol = 2

    # In the table with tax data, the values can be in the first column and
    # the fourth. The name of the data in third column.
    tax_values_icol = [0, 3]
    tax_name_icol = 2
    def __init__(self, siren, year, url):
        self.data = {'siren':siren,
                     'year': year,
                     'zone_type': self.zone_type,
                     'url': url}

    def has_taxes(self):
        return True

    def population(self, hxs):
        pop = self.table1(hxs).select('.//tr[position()=2]').re(r': ([\d\s]+) habitants')[0]
        return int(pop.replace(' ', ''))


    def tax_basis(self, hxs):
        return self.parse_one_tax_info(hxs, 'basis', self.tax_values_icol[0], 4, 11)

    def tax_cuts_on_deliberation(self, hxs):
        return self.parse_one_tax_info(hxs, 'cuts_on_deliberation', self.tax_values_icol[1], 4, 11)

    def tax_revenues(self, hxs):
        return self.parse_one_tax_info(hxs, 'value', self.tax_values_icol[0], 13, 20)

    def tax_rates(self, hxs):
        return self.parse_one_tax_info(hxs, 'rate', self.tax_values_icol[1], 13, 20, is_percent=True)

    def repartition_taxes(self, hxs):
        return self.parse_one_tax_info(hxs, 'value', self.tax_values_icol[0], 22, 25)

class DepartmentParser(CityParser):
    zone_type = 'department'
    account = department_account

    table1_ix = 5
    table2_ix = 6
    finance_value_icol = 1
    finance_name_icol = 0
    tax_values_icol = [0, 4]
    tax_name_icol = 3

    def name(self, hxs):
        xpath =  '//body/table[position()=3]/tr[position()=1]/td/span/text()'
        return hxs.select(xpath).extract()[0].split('SITUATION FINANCIERE du DEPARTEMENT de')[1].strip()

    def population(self, hxs):
        xpath =  '//body/table[position()=4]/tr[position()=1]/td/text()'
        pop = hxs.select(xpath).re(r': ([\d\s]+)\xa0')[0]
        return int(pop.replace(' ', ''))

    def has_taxes(self):
        return True

    def tax_basis(self, hxs):
        return self.parse_one_tax_info(hxs, 'basis', self.tax_values_icol[0], 4, 6)

    def tax_cuts_on_deliberation(self, hxs):
        return self.parse_one_tax_info(hxs, 'cuts_on_deliberation', self.tax_values_icol[1], 4, 6)

    def tax_revenues(self, hxs):
        return self.parse_one_tax_info(hxs, 'value', self.tax_values_icol[0], 8, 9)

    def tax_rates(self, hxs):
        return self.parse_one_tax_info(hxs, 'rate', self.tax_values_icol[1], 8, 9, is_percent=True)

    def repartition_taxes(self, hxs):
        # TODO: add parsing of cuts_on_deliberation
        return self.parse_one_tax_info(hxs, 'value', self.tax_values_icol[0], 11, 13)

class RegionParser(DepartmentParser):
    zone_type = 'region'
    account = region_account
    tax_name_icol = 1

    def name(self, hxs):
        xpath =  '//body/table[position()=3]/tr[position()=1]/td/span/text()'
        name = hxs.select(xpath).extract()[0]
        return name.split('SITUATION FINANCIERE de la ')[1].strip()

    def tax_basis(self, hxs):
        return {}

    def tax_cuts_on_deliberation(self, hxs):
        return self.parse_one_tax_info(hxs, 'cuts_on_deliberation', self.tax_values_icol[0], 3, 4)

    def tax_rates(self, hxs):
        return {}

    def tax_revenues(self, hxs):
        return {}

    def repartition_taxes(self, hxs):
        return self.parse_one_tax_info(hxs, 'value', self.tax_values_icol[0], 6, 8)



