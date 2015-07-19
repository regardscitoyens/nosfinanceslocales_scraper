# -*- coding: utf-8 -*-

from document_mapper import DocumentMapper

from .finance import (
    CityFinanceParser,
    EPCIFinanceParser,
    DepartmentFinanceParser,
    DepartmentFinance2013Parser,
    RegionFinanceParser
)

from .tax import (
    CityTaxParser,
    CityBefore2008TaxParser,
    EPCITaxParser,
    EPCI2008TaxParser,
    EPCI2010TaxParser,
    DepTaxParser,
    DepTax2008Parser,
    DepTax20092010Parser,
    RegTaxParser2008,
    RegTaxParser20092010,
    RegTaxParserAfter2011,
)


class BaseZoneParser(object):
    zone_type = ''
    account = None
    finance_table_id = 3
    finance_parser_cls = None
    tax_parser = None

    def __init__(self, insee_code, year, url):
        self.data = {'insee_code': insee_code,
                     'year': year,
                     'zone_type': self.zone_type,
                     'url': url}

    @property
    def finance_parser(self):
        return self.finance_parser_cls(self.account)

    def parse(self, hxs):
        data = self.data.copy()
        data.update(self.finance_parser.parse(hxs))
        data.update(self.tax_parser.parse(hxs))
        return data


class RegionZoneParser(BaseZoneParser):
    zone_type = 'region'
    account = None
    finance_parser_cls = RegionFinanceParser

    def __init__(self, insee_code, year, url):
        super(RegionZoneParser, self).__init__(insee_code, year, url)

        if int(self.data['year']) == 2008:
            self.tax_parser = RegTaxParser2008(self.account)
        elif int(self.data['year']) < 2011:
            self.tax_parser = RegTaxParser20092010(self.account)
        else:
            self.tax_parser = RegTaxParserAfter2011(self.account)


class DepartmentZoneParser(BaseZoneParser):
    zone_type = 'department'

    def __init__(self, insee_code, year, url):
        super(DepartmentZoneParser, self).__init__(insee_code, year, url)
        year = int(self.data['year'])
        self.finance_parser_cls = DepartmentFinanceParser
        if year >= 2013:
            self.account = DocumentMapper("data/mapping/department_2013.yaml")
            self.tax_parser = DepTaxParser(self.account)
            self.finance_parser_cls = DepartmentFinance2013Parser
        elif 2013 > year > 2010:
            self.account = DocumentMapper("data/mapping/department_2011.yaml")
            self.tax_parser = DepTaxParser(self.account)
        elif year == 2010:
            self.account = DocumentMapper("data/mapping/department_2010.yaml")
            self.tax_parser = DepTax20092010Parser(self.account)
        elif 2010 > year > 2008:
            self.account = DocumentMapper("data/mapping/department_2009.yaml")
            self.tax_parser = DepTax20092010Parser(self.account)
        elif year == 2008:
            self.account = DocumentMapper("data/mapping/department_2008.yaml")
            self.tax_parser = DepTax2008Parser(self.account)


class EPCIZoneParser(BaseZoneParser):
    zone_type = 'epci'
    account = None
    finance_parser_cls = EPCIFinanceParser

    def __init__(self, insee_code, year, url, siren):
        super(EPCIZoneParser, self).__init__(insee_code, year, url)
        self.data['siren'] = siren

        if int(self.data['year']) < 2009:
            self.tax_parser = EPCI2008TaxParser(self.account)
        elif int(self.data['year']) < 2011:
            self.tax_parser = EPCI2010TaxParser(self.account)
        else:
            self.tax_parser = EPCITaxParser(self.account)


class CityZoneParser(BaseZoneParser):
    """Parser of city html page"""
    zone_type = 'city'
    finance_parser_cls = CityFinanceParser

    def __init__(self, insee_code, year, url):
        super(CityZoneParser, self).__init__(insee_code, year, url)

        if int(self.data['year']) > 2011:
            self.account = DocumentMapper("data/mapping/city_2012.yaml")
            self.tax_parser = CityTaxParser(self.account)
        elif 2008 < int(self.data['year']) < 2012:
            self.account = DocumentMapper("data/mapping/city_2009.yaml")
            self.tax_parser = CityTaxParser(self.account)
        elif int(self.data['year']) < 2009:
            self.account = DocumentMapper("data/mapping/city_2000.yaml")
            self.tax_parser = CityBefore2008TaxParser(self.account)



