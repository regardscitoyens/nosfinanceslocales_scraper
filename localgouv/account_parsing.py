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
        return None

class CityParser(object):
    """Parser of city html page"""
    zone_type = 'city'
    account = city_account

    table1_ix = 3

    # In the table with financial data, the values we want to scrap are in 
    # the first columns, the name of the data is in the third column.
    finance_value_icol = 0
    finance_name_icol = 3

    def __init__(self, insee_code, year, url):
        self.data = {'insee_code':insee_code,
                     'year': year,
                     'zone_type': self.zone_type,
                     'url': url}

    def parse(self, response):
        """Parse html account table of a city for a given year
        crawled from http://alize2.finances.gouv.fr.
        Return a dictionnary which contains scraped data"""
        hxs = HtmlXPathSelector(response)

        data = self.data.copy()
        data['population'] = self.population(hxs)
        data['name'] = self.name(hxs)

        data.update(self.finance(hxs))
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
            targets = self.account.find_node(name=name)
            if targets and 'type' not in self.account.nodes[targets[0]]:
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
        # For years > 2008, we have also tax data
        if int(self.data['year']) > 2008:
            return After2008TaxParser(self.account).parse(hxs)
        else:
            return Before2008TaxParser(self.account).parse(hxs)

class TaxParser(object):
    tax_values_icol=(0,4)
    def __init__(self, account, table_ix=4):
        # In the table with tax data, the values can be in the first column and
        # the fourth. The name of the data in third column.
        self.account = account
        self.table_ix = table_ix

    def table(self, hxs):
        """Select table where we have tax data"""
        return hxs.select('//body/table[position()=%s]'%self.table_ix)

class After2008TaxParser(TaxParser):
    # Define all taxes
    # [name of tax info, start row, end row, col index of name of tax, is_percent]
    basis = ['basis', 0, 4, 9, 3, False]
    cuts_on_deliberation = ['cuts_on_deliberation', 4, 4, 9, 3, False]
    value = ['value', 0, 10, 16, 3, False]
    rate = ['rate', 4, 10, 16, 3, True]
    repartition_cuts_on_deliberation = ['cuts_on_deliberation', 4, 18, 21, 3, False]
    repartition_value = ['value', 0, 18, 21, 3, False]

    def parse(self, hxs):
        data = {}
        for tax in [self.basis, self.cuts_on_deliberation, self.value, self.rate,
                    self.repartition_cuts_on_deliberation, self.repartition_value]:
            if tax:
                data.update(self.parse_tax_info(hxs, *tax))
        return data

    def parse_tax_info(self, hxs, info_name, icol_value, start_row, end_row, tax_name_icol, is_percent):
        data = {}
        for row in self.table(hxs).select('.//tr')[start_row:end_row]:
            tds = row.select('.//td')
            if len(tds) <= max(icol_value, tax_name_icol):
                continue
            name = tds[tax_name_icol].select('./text()').extract()[0].strip()
            targets = self.account.find_node(name=name, type='section')
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

class Before2008TaxParser(TaxParser):
    def __init__(self, *args, **kwargs):
        super(Before2008TaxParser, self).__init__(*args, **kwargs)
        self.tax_name_icol = 3
        self.table_ix = 3
        self.tax_values_icol = (0, 4)
    def parse(self, hxs):
        data = {}
        tax_names = ['home_tax', 'property_tax', 'land_property_tax', 'business_tax']
        for tr, tax_name in zip(self.table(hxs).select('.//tr')[20:24], tax_names):
            tds = tr.select('.//td/text()')
            name = tds[self.tax_name_icol].extract().strip()
            value = convert_value(tds[self.tax_values_icol[0]].extract()) * 1000
            rate = convert_value(tds[self.tax_values_icol[1]].extract()) / 100
            data['%s_%s'%(tax_name, 'value')] = value
            data['%s_%s'%(tax_name, 'rate')] = rate
        return data

class EPCIParser(CityParser):
    zone_type = 'epci'
    account = epci_account

    # In the table with financial data, the values we want to scrap are in 
    # the first columns, the name of the data is in the third column.
    finance_value_icol = 0
    finance_name_icol = 2

    def __init__(self, siren, year, url):
        self.data = {'siren':siren,
                     'year': year,
                     'zone_type': self.zone_type,
                     'url': url}

    def population(self, hxs):
        pop = self.table1(hxs).select('.//tr[position()=2]').re(r': ([\d\s]+) habitants')[0]
        return int(pop.replace(' ', ''))

    def taxes(self, hxs):
        if int(self.data['year']) < 2009:
            return EPCI2008TaxParser(self.account).parse(hxs)
        elif int(self.data['year']) < 2011:
            return EPCI2010TaxParser(self.account).parse(hxs)
        else:
            return EPCITaxParser(self.account).parse(hxs)

class EPCITaxParser(After2008TaxParser):
    basis = ['basis', 0, 4, 11, 2, False]
    cuts_on_deliberation = ['cuts_on_deliberation', 3, 4, 11, 2, False]
    value = ['value', 0, 13, 20, 2, False]
    rate = ['rate', 3, 13, 20, 2, True]
    repartition_cuts_on_deliberation = None
    repartition_value = ['value', 0, 22, 25, 2, False]

class EPCI2010TaxParser(After2008TaxParser):
    basis = ['basis', 0, 4, 10, 2, False]
    cuts_on_deliberation = ['cuts_on_deliberation', 3, 4, 10, 2, False]
    value = ['value', 0, 12, 18, 2, False]
    rate = ['rate', 3, 12, 18, 2, True]
    repartition_cuts_on_deliberation = None
    repartition_value = ['value', 0, 18, 21, 2, False]

class EPCI2008TaxParser(After2008TaxParser):
    basis = ['basis', 0, 4, 9, 1, False]
    cuts_on_deliberation = None
    value = ['value', 0, 12, 18, 2, False]
    rate = ['rate', 3, 12, 18, 2, True]
    repartition_cuts_on_deliberation = None
    repartition_value = None

class DepartmentParser(CityParser):
    zone_type = 'department'
    account = department_account

    table1_ix = 5
    finance_value_icol = 1
    finance_name_icol = 0

    def name(self, hxs):
        xpath =  '//body/table[position()=3]/tr[position()=1]/td/span/text()'
        return hxs.select(xpath).extract()[0].split('SITUATION FINANCIERE du DEPARTEMENT de')[1].strip()

    def population(self, hxs):
        xpath =  '//body/table[position()=4]/tr[position()=1]/td/text()'
        pop = hxs.select(xpath).re(r': ([\d\s]+)\xa0')[0]
        return int(pop.replace(' ', ''))

    def taxes(self, hxs):
        if int(self.data['year']) > 2010:
            return DepTaxParser(self.account, table_ix=6).parse(hxs)
        elif int(self.data['year']) > 2008:
            return DepTax20092010Parser(self.account, table_ix=6).parse(hxs)
        else:
            return DepTax2008Parser(self.account, table_ix=6).parse(hxs)

class DepTaxParser(After2008TaxParser):
    basis = ['basis', 0, 4, 6, 3, False]
    cuts_on_deliberation = ['cuts_on_deliberation', 4, 4, 6, 3, False]
    value = ['value', 0, 8, 9, 3, False]
    rate = ['rate', 4, 8, 9, 3, True]
    repartition_cuts_on_deliberation = None
    repartition_value = ['value', 0, 11, 13, 1, False]

class DepTax20092010Parser(DepTaxParser):
    basis = ['basis', 0, 4, 8, 3, False]
    cuts_on_deliberation = None
    value = ['value', 0, 9, 14, 3, False]
    rate = ['rate', 4, 9, 14, 3, True]
    repartition_value = None

class DepTax2008Parser(DepTax20092010Parser):
    basis = ['basis', 0, 3, 8, 2, False]

class RegionParser(DepartmentParser):
    zone_type = 'region'
    account = region_account

    def name(self, hxs):
        xpath =  '//body/table[position()=3]/tr[position()=1]/td/span/text()'
        name = hxs.select(xpath).extract()[0]
        return name.split('SITUATION FINANCIERE de la ')[1].strip()

    def taxes(self, hxs):
        if int(self.data['year']) == 2008:
            return RegTaxParser2008(self.account, table_ix=6).parse(hxs)
        elif int(self.data['year']) < 2011:
            return RegTaxParser20092010(self.account, table_ix=6).parse(hxs)
        else:
            return RegTaxParserAfter2011(self.account, table_ix=6).parse(hxs)

class RegTaxParserAfter2011(DepTaxParser):
    basis = None
    cuts_on_deliberation = ['cuts_on_deliberation', 0, 3, 4, 1, False]
    value = None
    rate = None
    repartition_value = ['value', 0, 6, 8, 1, False]

class RegTaxParser20092010(DepTaxParser):
    basis = ['basis', 0, 4, 7, 3, False]
    cuts_on_deliberation = ['cuts_on_deliberation', 4, 4, 7, 3, False]
    value = ['value', 0, 8, 12, 3, False]
    rate = ['rate', 4, 8, 12, 3, True]
    repartition_cuts_on_deliberation = None
    repartition_value = None

class RegTaxParser2008(RegTaxParser20092010):
    basis = ['basis', 0, 4, 7, 2, False]
    cuts_on_deliberation = ['cuts_on_deliberation', 4, 4, 7, 2, False]
    value = ['value', 0, 9, 13, 3, False]
    rate = ['rate', 4, 9, 13, 3, True]
    repartition_value = ['value', 0, 11, 13, 2, False]
