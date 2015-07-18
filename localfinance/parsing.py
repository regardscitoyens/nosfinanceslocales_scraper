# -*- coding: utf-8 -*-

import re
import yaml
import codecs

from difflib import SequenceMatcher

from .utils import clean_name
from .utils import sanitize_value


class DocumentMapping(object):
    def __init__(self, yaml_file):
        self.mapping = yaml.load(codecs.open(yaml_file, 'r', encoding="utf-8"))
        self.sections = [s.strip().lower() for s in self.mapping.keys()]

    def find_node(self, section, name):
        if not section or section not in self.mapping:
            return None

        for key, value in self.mapping[section].items():
            if name.lower() in value.lower():
                return key

    def find_tax(self, name):
        taxes = []
        for key, value in self.mapping['tax']['types'].items():
            s = SequenceMatcher(None, name.lower(), value.lower())
            if s.ratio() > 0.5:
                taxes.append((s.ratio(), key))
        return sorted(taxes)[-1][1] if taxes else []

    def is_section(self, name):
        return name.strip().lower() in self.sections


class FinanceParser(object):
    # In the table with financial data, the values we want to scrap are in
    # the first columns, the name of the data is in the third column.
    finance_value_icol = 0
    finance_name_icol = 3

    table_id = 3

    def __init__(self, account):
        self.account = account

    def name(self, hxs):
        return self.table(hxs).xpath('.//tr[position()=2]/td[position()=2]/text()').extract()[0]

    def population(self, hxs):
        raise NotImplementedError

    def table(self, hxs):
        """Select table where we have name, population, and finance data"""
        return hxs.xpath('//body/table[position()=%s]' % self.table_id)

    def parse(self, hxs):
        # - the value is always in the column finance_value_icol of the table.
        #   If there is no value, this is just section of the budget
        # - the name of the financial data is defined the column finance_name_icol

        data = {
            'population': self.population(hxs),
            'name': self.name(hxs)
        }

        current_section = None

        for tr in self.table(hxs).xpath('.//tr')[1:]:
            ths = tr.xpath('.//th')

            if len(ths) == 1:
                section = ths[0].xpath('.//text()').extract()[0]
                if self.account.is_section(section):
                    current_section = section
                    continue

                if not self.account.find_node(current_section, section):
                    continue

            # In some weird cases, selecting directly by select('.//td/text()')
            # does not work
            tds = tr.xpath('.//td')

            if len(tds) < 4:
                continue

            names = [n.strip() for n in tds[self.finance_name_icol].xpath('.//text()').extract() if n.strip()]

            # if there are no names in td tags, try to find some in th tags
            if not names:
                names = [n.strip() for n in ths[0].xpath('.//text()').extract() if n.strip()]

            if not names:
                continue

            name = clean_name(names[0])
            target = self.account.find_node(current_section, name)
            if target:
                try:
                    value = sanitize_value(tds[self.finance_value_icol].xpath('.//text()').extract()[0]) * 1000
                    if value is not None:
                        data[target] = value
                except IndexError:
                    print "no value for node %s " % name

        return data


class DepartmentFinanceParser(FinanceParser):
    table_id = 5
    finance_value_icol = 1
    finance_name_icol = 0

    def name(self, hxs):
        xpath = '//body/table[position()=3]/tr[position()=1]/td/span/text()'
        text = hxs.xpath(xpath).extract()[0]
        return re.split('SITUATION FINANCIERE du DEPARTEMENT (de|du) ', text)[-1]

    def population(self, hxs):
        xpath = '//body/table[position()=4]/tr[position()=1]/td/text()'
        pop = hxs.xpath(xpath).re(r': ([\d\s]+)\xa0')[0]
        return int(pop.replace(' ', ''))


class RegionFinanceParser(DepartmentFinanceParser):
    def name(self, hxs):
        xpath = '//body/table[position()=3]/tr[position()=1]/td/span/text()'
        name = hxs.xpath(xpath).extract()[0]
        return name.split('SITUATION FINANCIERE de la ')[1].strip()


class CityFinanceParser(FinanceParser):
    tr_name_position = 3

    def population(self, hxs):
        pop = self.table(hxs).xpath('.//tr[position()=%s]' % self.tr_name_position)
        pop = pop.re(r': ([\d\s]+) habitants')[0]
        return int(pop.replace(' ', ''))


class EPCIFinanceParser(CityFinanceParser):
    finance_name_icol = 2
    tr_name_position = 2


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
        for row in hxs.xpath('.//tr')[taxinfo.start_row:taxinfo.end_row]:
            tds = row.xpath('.//td')

            if len(tds) <= max(taxinfo.value_col, taxinfo.name_col):
                continue

            name = clean_name(tds[taxinfo.name_col].xpath('./text()').extract()[0])

            target = self.account.find_tax(name)

            if target:
                str_val = tds[taxinfo.value_col].xpath('./text()').extract()[0].strip()
                try:
                    val = sanitize_value(str_val)
                except ValueError:
                    print u"There is no valid value for the node %s - %s" % (target, str_val)
                    continue
                if taxinfo.name == 'rate':
                    val /= 100.
                else:
                    val *= 1000
                key = "%s_%s" % (target, taxinfo.name)
                data[key] = val

        return data


class TaxParser(object):
    table_id = 4
    _infos = []

    def __init__(self, account):
        self.account = account

    def table(self, hxs):
        """Select table where we have tax data"""
        return hxs.xpath('//body/table[position()=%s]' % self.table_id)

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
        TaxInfo('cuts_on_deliberation', 4, 8, 3, 4),
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


class BaseZoneParser(object):
    zone_type = ''
    account = None
    finance_table_id = 3
    finance_parser_cls = None

    def __init__(self, insee_code, year, url):
        self.data = {'insee_code': insee_code,
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


class RegionZoneParser(BaseZoneParser):
    zone_type = 'region'
    account = None
    finance_parser_cls = RegionFinanceParser

    @property
    def tax_parser(self):
        if int(self.data['year']) == 2008:
            return RegTaxParser2008(self.account)
        elif int(self.data['year']) < 2011:
            return RegTaxParser20092010(self.account)
        else:
            return RegTaxParserAfter2011(self.account)


class DepartmentZoneParser(BaseZoneParser):
    zone_type = 'department'
    account = DocumentMapping("data/mapping/department_2009.yaml")
    finance_parser_cls = DepartmentFinanceParser

    @property
    def tax_parser(self):
        if int(self.data['year']) > 2010:
            return DepTaxParser(self.account)
        elif int(self.data['year']) > 2008:
            return DepTax20092010Parser(self.account)
        else:
            return DepTax2008Parser(self.account)


class EPCIZoneParser(BaseZoneParser):
    zone_type = 'epci'
    account = None
    finance_parser_cls = EPCIFinanceParser

    def __init__(self, siren, year, url):
        self.data = {'siren': siren,
                     'year': year,
                     'zone_type': self.zone_type,
                     'url': url}

    @property
    def tax_parser(self):
        if int(self.data['year']) < 2009:
            return EPCI2008TaxParser(self.account)
        elif int(self.data['year']) < 2011:
            return EPCI2010TaxParser(self.account)
        else:
            return EPCITaxParser(self.account)


class CityZoneParser(BaseZoneParser):
    """Parser of city html page"""
    zone_type = 'city'
    account = DocumentMapping("data/mapping/city_2012.yaml")
    finance_parser_cls = CityFinanceParser

    @property
    def tax_parser(self):
        # For years > 2008, we have also tax data
        if int(self.data['year']) > 2008:
            return CityTaxParser(self.account)
        else:
            return CityBefore2008TaxParser(self.account)


