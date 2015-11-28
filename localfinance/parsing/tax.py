# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from ..utils import clean_name
from ..utils import sanitize_value


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

            name = clean_name(' '.join(tds[taxinfo.name_col].xpath('.//text()').extract()).strip())

            target = self.account.find_tax(name)

            if target:
                str_val = tds[taxinfo.value_col].xpath('./text()').extract()[0].strip()
                try:
                    val = sanitize_value(str_val)
                except ValueError:
                    logger.warning(u"There is no valid value for the node %s '%s'" % (target, str_val))
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
        TaxInfo('cuts_on_deliberation', 3, 8, 2, 3),
    ]


class EPCITaxParser(TaxParser):
    _infos = [
        TaxInfo('basis', 4, 11, 2, 0),
        TaxInfo('cuts_on_deliberation', 4, 11, 2, 3),
        TaxInfo('value', 13, 20, 2, 0),
        TaxInfo('rate', 13, 20, 2, 3),
        TaxInfo('value', 21, 25, 2, 0),
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
