# -*- coding: utf-8 -*-

from .account_network import (
    city_account,
    epci_account,
    department_account,
    region_account
)

def sanitize_value(val):
    """Remove crap from val string and then convert it into float"""
    val = val.replace(u'\xa0', '')\
             .replace(',', '.')\
             .replace(u'\xa0', '')\
             .replace(' ', '')
    # positive or negative multiplier
    mult = 1

    if '-' in val and len(val) > 1:
        mult = -1
        val = val.replace('-', '')
    elif '-' in val:
        val = '0'

    if val is not None:
        if '%' in val:
            val = float(val.replace('%', ''))
        return float(val) * mult

def sanitize_name(name):
    return name.replace('dont', '').replace(':', '').replace('+', '').strip()
#
#
#
# Finance Parsers
#
#
#

class FinanceParser(object):
     # In the table with financial data, the values we want to scrap are in 
    # the first columns, the name of the data is in the third column.
    finance_value_icol = 0
    finance_name_icol = 3

    table_id = 3

    def __init__(self, account):
        self.account = account

    def name(self, hxs):
        return self.table(hxs).select('.//tr[position()=2]/td[position()=2]/text()').extract()[0]

    def population(self, hxs):
        raise NotImplementedError

    def table(self, hxs):
        """Select table where we have name, population, and finance data"""
        return hxs.select('//body/table[position()=%s]'%self.table_id)

    def parse(self, hxs):
        # - the value is always in the column finance_value_icol of the table.
        #   If there is no value, this is just section of the budget
        # - the name of the financial data is defined the column finance_name_icol

        data = {
            'population': self.population(hxs),
            'name': self.name(hxs)
        }

        for tr in self.table(hxs).select('.//tr')[2:]:
            # In some weird cases, selecting directly by select('.//td/text()')
            # does not work
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
            name = sanitize_name(name_td[0])
            targets = self.account.find_node(name=name)
            if targets and 'type' not in self.account.nodes[targets[0]]:
                target = targets[0]
                try:
                    value = sanitize_value(tds[self.finance_value_icol]\
                        .select('.//text()').extract()[0]) * 1000
                    if value is not None:
                        data[target] = value
                except IndexError:
                    print "no value for node %s "%name
            else:
                print "There is no node of name %s "%name

        return data

class DepartmentFinanceParser(FinanceParser):
    table_id = 5
    finance_value_icol = 1
    finance_name_icol = 0
    def name(self, hxs):
        xpath =  '//body/table[position()=3]/tr[position()=1]/td/span/text()'
        return hxs.select(xpath).extract()[0].split('SITUATION FINANCIERE du DEPARTEMENT de')[1].strip()

    def population(self, hxs):
        xpath =  '//body/table[position()=4]/tr[position()=1]/td/text()'
        pop = hxs.select(xpath).re(r': ([\d\s]+)\xa0')[0]
        return int(pop.replace(' ', ''))

class RegionFinanceParser(DepartmentFinanceParser):
    def name(self, hxs):
        xpath =  '//body/table[position()=3]/tr[position()=1]/td/span/text()'
        name = hxs.select(xpath).extract()[0]
        return name.split('SITUATION FINANCIERE de la ')[1].strip()

class CityFinanceParser(FinanceParser):
    tr_name_position = 3
    def population(self, hxs):
        pop = self.table(hxs).select('.//tr[position()=%s]'%self.tr_name_position)
        pop = pop.re(r': ([\d\s]+) habitants')[0]
        return int(pop.replace(' ', ''))

class EPCIFinanceParser(CityFinanceParser):
    finance_name_icol = 2
    tr_name_position = 2

#
#
#
#
# Tax parsing: much more complicated
#
#
#

class TaxInfo(object):
    def __init__(self, name, start_row, end_row, name_col, value_col):
        self.name = name
        self.start_row = start_row
        self.end_row = end_row
        self.name_col = name_col
        self.value_col = value_col

class TaxInfoParser(object):
    def __init__(self, account, taxinfo):
        self.account = account
        self.taxinfo = taxinfo

    def parse(self, hxs):
        data = {}
        taxinfo = self.taxinfo
        for row in hxs.select('.//tr')[taxinfo.start_row:taxinfo.end_row]:
            tds = row.select('.//td')
            if len(tds) <= max(taxinfo.value_col, taxinfo.name_col):
                continue
            name = sanitize_name(tds[taxinfo.name_col].select('./text()').extract()[0])
            targets = self.account.find_node(name=name, type='section')
            if targets:
                target = targets[0]
                str_val = tds[taxinfo.value_col].select('./text()').extract()[0].strip()
                try:
                    val = sanitize_value(str_val)
                except ValueError:
                    print u"There is no valid value for the node %s"%target
                    continue
                if taxinfo.name == 'rate':
                    val = val / 100.
                else:
                    val = val * 1000
                key = "%s_%s"%(target,taxinfo.name)
                data[key] = val
            else:
                print "There is no node of name %s "%name
        return data

class TaxParser(object):
    table_id = 4

    def __init__(self, account):
        self.account = account

    def table(self, hxs):
        """Select table where we have tax data"""
        return hxs.select('//body/table[position()=%s]'%self.table_id)

    @property
    def infos(self):
        return self._infos

    def parse(self, hxs):
        data = {}
        for info in self.infos:
            parser = TaxInfoParser(self.account, info)
            data.update(parser.parse(self.table(hxs)))
        return data

class RegTaxParserAfter2011(TaxParser):
    table_id = 6
    _infos = [
        TaxInfo('cuts_on_deliberation', 3, 4, 1, 0),
        TaxInfo('value', 6, 8, 1, 0),
    ]

class RegTaxParser20092010(RegTaxParserAfter2011):
    _infos = [
        TaxInfo('basis', 4, 7, 3, 0),
        TaxInfo('cuts_on_deliberation', 4, 7, 3, 4),
        TaxInfo('value', 8, 12, 3, 0),
        TaxInfo('rate', 8, 12, 3, 4),
    ]

class RegTaxParser2008(RegTaxParserAfter2011):
    _infos = [
        TaxInfo('basis', 4, 7, 2, 0),
        TaxInfo('cuts_on_deliberation', 4, 7, 2, 4),
        TaxInfo('value', 9, 13, 3, 0),
        TaxInfo('rate', 9, 13, 3, 4),
        TaxInfo('value', 11, 13, 2, 0),
    ]

class DepTaxParser(TaxParser):
    table_id = 6
    _infos = [
        TaxInfo('basis', 4, 6, 3, 0),
        TaxInfo('cuts_on_deliberation', 4, 6, 3, 4),
        TaxInfo('value', 8, 9, 3, 0),
        TaxInfo('rate', 8, 9, 3, 4),
        TaxInfo('value', 11, 13, 1, 0),
    ]

class DepTax20092010Parser(DepTaxParser):
    _infos = [
        TaxInfo('basis', 4, 8, 3, 0),
        TaxInfo('value', 9, 14, 3, 0),
        TaxInfo('rate', 9, 14, 3, 4),
    ]

class DepTax2008Parser(DepTaxParser):
    _infos = [
        TaxInfo('basis', 3, 8, 2, 0),
        TaxInfo('value', 9, 14, 3, 0),
        TaxInfo('rate', 9, 14, 3, 4),
    ]

class EPCITaxParser(TaxParser):
    _infos = [
        TaxInfo('basis', 4, 11, 2, 0),
        TaxInfo('cuts_on_deliberation', 4, 11, 2, 3),
        TaxInfo('value', 13, 20, 2, 0),
        TaxInfo('rate', 13, 20, 2, 3),
        TaxInfo('value', 22, 25, 2, 0),
    ]

class EPCI2010TaxParser(TaxParser):
    _infos = [
        TaxInfo('basis', 4, 10, 2, 0),
        TaxInfo('cuts_on_deliberation', 4, 10, 2, 3),
        TaxInfo('value', 12, 18, 2, 0),
        TaxInfo('rate', 12, 18, 2, 3),
        TaxInfo('value', 18, 21, 2, 0),
    ]

class EPCI2008TaxParser(TaxParser):
    _infos = [
        TaxInfo('basis', 4, 9, 1, 0),
        TaxInfo('value', 12, 18, 2, 0),
        TaxInfo('rate', 12, 18, 2, 3),
    ]

class CityTaxParser(TaxParser):
    _infos = [
        TaxInfo('basis', 4, 9, 3, 0),
        TaxInfo('cuts_on_deliberation', 4, 9, 3, 4),
        TaxInfo('value', 10, 16, 3, 0),
        TaxInfo('rate', 10, 16, 3, 4),
        TaxInfo('cuts_on_deliberation', 18, 21, 3, 4),
        TaxInfo('value', 18, 21, 3, 0),
    ]

class CityBefore2008TaxParser(TaxParser):
    table_id = 3
    _infos = [
        TaxInfo('value', 20, 24, 3, 0),
        TaxInfo('rate', 20, 24, 3, 4),
    ]

#
#
#
# Zone Parser: parse finance and tax
#
#
#




class BaseParser(object):
    zone_type = ''
    account = None
    finance_table_id = 3
    finance_parser_cls = None

    def __init__(self, code, year, url):
        self.data = {'code':code,
                     'year': year,
                     'zone_type': self.zone_type,
                     'url': url}

    @property
    def finance_parser(self):
        return self.finance_parser_cls(self.account)

    @property
    def tax_parser(self):
        return NotImplementedError

    def parse(self, hxs):
        data = self.data.copy()
        data.update(self.finance_parser.parse(hxs))
        data.update(self.tax_parser.parse(hxs))
        return data


class RegionParser(BaseParser):
    zone_type = 'region'
    account = region_account
    finance_parser_cls = RegionFinanceParser

    @property
    def tax_parser(self):
        if int(self.data['year']) == 2008:
            return RegTaxParser2008(self.account)
        elif int(self.data['year']) < 2011:
            return RegTaxParser20092010(self.account)
        else:
            return RegTaxParserAfter2011(self.account)

class DepartmentParser(BaseParser):
    zone_type = 'department'
    account = department_account
    finance_parser_cls = DepartmentFinanceParser

    @property
    def tax_parser(self):
        if int(self.data['year']) > 2010:
            return DepTaxParser(self.account)
        elif int(self.data['year']) > 2008:
            return DepTax20092010Parser(self.account)
        else:
            return DepTax2008Parser(self.account)

class EPCIParser(BaseParser):
    zone_type = 'epci'
    account = epci_account
    finance_parser_cls = EPCIFinanceParser

    @property
    def tax_parser(self):
        if int(self.data['year']) < 2009:
            return EPCI2008TaxParser(self.account)
        elif int(self.data['year']) < 2011:
            return EPCI2010TaxParser(self.account)
        else:
            return EPCITaxParser(self.account)

class CityParser(BaseParser):
    """Parser of city html page"""
    zone_type = 'city'
    account = city_account
    finance_parser_cls = CityFinanceParser

    @property
    def tax_parser(self):
        # For years > 2008, we have also tax data
        if int(self.data['year']) > 2008:
            return CityTaxParser(self.account)
        else:
            return CityBefore2008TaxParser(self.account)


