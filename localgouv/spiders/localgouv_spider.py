# -*- coding: utf-8 -*-

import pandas as pd
import re

from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from ..account_parsing import (
    CityParser,
    EPCIParser,
    DepartmentParser,
    RegionParser
)

from ..item import (
    CityFinancialData,
    EPCIFinancialData,
    DepartmentFinancialData,
    RegionFinancialData
)

class LocalGouvFinanceSpider(BaseSpider):
    """Basic spider which crawls all pages of finance of french towns, departments
    regions and EPCI.
    """
    name = "localgouv"
    domain = "http://alize2.finances.gouv.fr"
    allowed_domains = [domain]

    def __init__(self, year=2012, zone_type='city'):
        """Load insee code of every commune in france and generate all the urls to
        crawl."""
        self.start_urls = []
        if zone_type == 'city' or zone_type == 'all':
            self.start_urls += self.get_commune_urls(year)
        if zone_type == 'department' or zone_type == 'all':
            self.start_urls += self.get_dep_urls(year)
        if zone_type == 'region' or zone_type == 'all':
            self.start_urls += self.get_reg_urls(year)
        if zone_type == 'epci' or zone_type == 'all':
            self.start_urls += self.get_epci_urls(year)

    def get_dep_urls(self, year):
        insee_code_file = "./data/depts2013.txt"
        data = pd.io.parsers.read_csv(insee_code_file, '\t')
        data['DEP'] = uniformize_code(data, 'DEP')
        data['DEP'] = convert_dom_code(data)
        baseurl = "%s/departements/detail.php?dep=%%(DEP)s&exercice=%s"%(self.domain, year)
        return [baseurl%row for __, row in data.iterrows()]

    def get_reg_urls(self, year):
        insee_code_file = "./data/reg2013.txt"
        data = pd.io.parsers.read_csv(insee_code_file, '\t')
        data['REGION'] = uniformize_code(data, 'REGION')
        # Special case for DOM as usual
        def set_dom_code(reg):
            if reg == '001':
                return '101'
            elif reg == '002':
                return '103'
            elif reg == '003':
                return '102'
            elif reg == '004':
                return '104'
            else:
                return reg
        data['REGION'] = data['REGION'].apply(set_dom_code)
        baseurl = "%s/regions/detail.php?reg=%%(REGION)s&exercice=%s"%(self.domain, year)
        return [baseurl%row for __, row in data.iterrows()]

    def get_epci_urls(self, year):
        """Build url to crawl from insee file provided here
        http://www.insee.fr/fr/methodes/default.asp?page=zonages/intercommunalite.htm"""
        xls = pd.ExcelFile('./data/epci-au-01-01-2013.xls')
        data = xls.parse('Composition communale des EPCI')
        data['siren'] = data[u'Établissement public à fiscalité propre'][1:]
        data = data.groupby('siren', as_index=False).first()
        data['dep'] = data[u'Département commune'].apply(get_dep_code_from_com_code)
        baseurl = "%s/communes/eneuro/detail_gfp.php?siren=%%(siren)s&dep=%%(dep)s&type=BPS&exercice=%s"%(self.domain, str(year))
        return [baseurl%row for __, row in data.iterrows()]

    def get_commune_urls(self, year):
        """
        The communes pages urls depends on 5 parameters:
        - COM: the insee code of the commune
        - DEP: the department code on 3 characters
        - type: type of financial data, BPS is for the whole data.
        - exercise: year of financial data
        """

        insee_code_file="./data/france2013.txt"
        data = pd.io.parsers.read_csv(insee_code_file, '\t')
        # XXX: insee_communes file contains also "cantons", filter out these lines
        mask = data['ACTUAL'].apply(lambda v: v in [1, 2, 3])
        data = data[mask]

        data['DEP'] = uniformize_code(data, 'DEP')
        data['COM'] = uniformize_code(data, 'COM')

        data['DEP'] = convert_dom_code(data)

        data['COM'] = data.apply(convert_city, axis=1)

        baseurl = "%s/communes/eneuro/detail.php?icom=%%(COM)s&dep=%%(DEP)s&type=BPS&param=0&exercice=%s"%(self.domain,str(year))
        return [baseurl%row for __, row in data.iterrows()]

    def parse(self, response):
        if "/communes/eneuro/detail_gfp.php" in response.url:
            return self.parse_epci(response)
        elif "/communes/eneuro/detail.php" in response.url:
            return self.parse_commune(response)
        elif "/departements/detail.php" in response.url:
            return self.parse_dep(response)
        elif "/regions/detail.php" in response.url:
            return self.parse_reg(response)

    def parse_commune(self, response):
        """Parse the response and return an Account object"""
        hxs = HtmlXPathSelector(response)
        icom, dep, year = re.search('icom=(\d{3})&dep=(\w{3})&type=\w{3}&param=0&exercice=(\d{4})', response.url).groups()
        # XXX: better to use the real insee code for later analysis, not icom and dep
        # in url.
        real_dep = dict([(val, key) for key, val in DOM_DEP_MAPPING.items()]).get(dep, dep[1:])
        real_com = icom if dep not in DOM_DEP_MAPPING.values() else icom[1:]
        parser = CityParser(real_dep+real_com, year, response.url)
        data = parser.parse(hxs)
        # convert account object to an Item instance.
        # WHY DO I NEED TO DO THAT SCRAPY ????
        item = CityFinancialData(data)
        return item

    def parse_epci(self, response):
        hxs = HtmlXPathSelector(response)
        siren, year = re.search('siren=(\d+)&dep=\w{3}&type=BPS&exercice=(\d{4})', response.url).groups()
        parser = EPCIParser(siren, year, response.url)
        data = parser.parse(hxs)
        item = EPCIFinancialData(data)
        return item

    def parse_dep(self, response):
        hxs = HtmlXPathSelector(response)
        dep, year = re.search('dep=(\w{3})&exercice=(\d{4})', response.url).groups()
        parser = DepartmentParser(dep, year, response.url)
        data = parser.parse(hxs)
        item = DepartmentFinancialData(data)
        return item

    def parse_reg(self, response):
        hxs = HtmlXPathSelector(response)
        dep, year = re.search('reg=(\w{3})&exercice=(\d{4})', response.url).groups()
        parser = RegionParser(dep, year, response.url)
        data = parser.parse(hxs)
        item = RegionFinancialData(data)
        return item

def uniformize_code(df, column):
    # Uniformize dep code and commune code to be on a string of length 3.
    def _uniformize_code(code):
        return ("00%s"%code)[-3:]
    return df[column].apply(_uniformize_code)


# Weird thing: department is not the same between insee data and gouverment's
# site for DOM.
# GUADELOUPE: 971 -> 101
# MARTINIQUE: 972 -> 103
# GUYANE:     973 -> 102
# REUNION:    974 -> 104
DOM_DEP_MAPPING = {
    '971': '101',
    '972': '103',
    '973': '102',
    '974': '104',
}
def convert_dom_code(df, column='DEP'):
    return df[column].apply(lambda code: DOM_DEP_MAPPING.get(code, code))

def get_dep_code_from_com_code(com):
    return DOM_DEP_MAPPING.get(str(com[:3]), ('0%s'%com)[:3])

# Another strange thing, DOM cities have an insee_code on 2 digits in the
# insee file. We need to add a third digit before these two to crawl the
# right page. This third digit is find according to this mapping:
# GUADELOUPE: 1
# MARTINIQUE: 2
# GUYANE: 3
# REUNION: 4
DOM_CITY_DIGIT_MAPPING = {'101': 1, '103': 2, '102': 3, '104': 4}
def convert_city(row):
    if row['DEP'] not in ['101', '102', '103', '104']:
        return row['COM']
    first_digit = str(DOM_CITY_DIGIT_MAPPING.get(row['DEP']))
    return first_digit + row['COM'][1:]

