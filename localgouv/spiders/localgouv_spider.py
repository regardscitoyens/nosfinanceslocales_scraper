# -*- coding: utf-8 -*-

import pandas as pd
import re

from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from ..account_parsing import parse_city_page_account
from ..item import CityFinancialData

class LocalGouvFinanceSpider(BaseSpider):
    """Basic spider which crawls all pages of finance of french towns.
    The pages' urls depends on 5 parameters:
        - COM: the insee code of the commune
        - DEP: the department code on 3 character
        - type: type of financial stuff, BPS is for the whole data.
        - param: ?
        - exercise: year of financial data
        """
    name = "localgouv"
    domain = "http://alize2.finances.gouv.fr"
    allowed_domains = [domain]

    def __init__(self, year=2012, com=True, depreg=False, epci=False):
        """Load insee code of every commune in france and generate all the urls to
        crawl."""
        self.start_urls = []
        if com:
            self.start_urls += self.get_commune_urls(year)
        if depreg:
            self.start_urls += self.get_depreg_urls(year)
        if epci:
            self.start_urls += self.get_epci_urls(year)

    def get_dep_and_region_urls(self, year):
        #TODO
        dep_baseurl = "%s/departements/detail.php?dep=%%(dep)s&exercice=%s"%(self.domain, year)
        reg_baseurl = "%s/regions/detail.php?reg=%%(reg)s&exercice=%s"%(self.domain, year)
        return []

    def get_epci_urls(self, year):
        xls = pd.ExcelFile('./data/epci-au-01-01-2013.xls')
        data = xls.parse('Composition communale des EPCI')
        data['siren'] = df[u'Établissement public à fiscalité propre'][1:]
        data['dep'] = df[u'Département commune'].apply(lambda r: ('0%s'%r)[:3])
        baseurl = "%s/communes/eneuro/detail_gfp.php?siren=%%(siren)s&dep=%%(dep)s&type=BPS&exercice=%s"%(self.domain, str(year))
        return [baseurl%row for __, row in data.iterrows()][1:]

    def get_commune_urls(self, year):
        insee_code_file="./data/france2013.txt"
        # XXX: insee_communes file contains also "cantons", filter out these lines
        # XXX: some departments are not crawled correctly: 75, 92, 93, 94 and maybe
        # others. Fix this.
        data = pd.io.parsers.read_csv(insee_code_file, '\t')
        mask = data['ACTUAL'].apply(lambda v: v in [1, 2, 3])
        data = data[mask]

        # Uniformize dep code and commune code to be on a string of length 3.
        def uniformize_code(code):
            return ("00%s"%code)[-3:]
        data['DEP'] = data['DEP'].apply(uniformize_code)
        data['COM'] = data['COM'].apply(uniformize_code)

        # Weird thing: department is not the same between insee data and gouverment's
        # site for DOM.
        # GUADELOUPE: 971 -> 101
        # MARTINIQUE: 972 -> 103
        # GUYANE:     973 -> 102
        # REUNION:    974 -> 104
        def convert_dep(code):
            return {
                '971': '101',
                '972': '103',
                '973': '102',
                '974': '104',
            }.get(code, code)
        data['DEP'] = data['DEP'].apply(convert_dep)
        # Another strange thing, DOM cities have an insee_code on 2 digits in the
        # insee file. We need to add a third digit before these two to crawl the
        # right page. This third digit is find according to this mapping:
        # GUADELOUPE: 1
        # MARTINIQUE: 2
        # GUYANE: 3
        # REUNION: 4
        digit_mapping = {'101': 1, '103': 2, '102': 3, '104': 4}
        def convert_city(row):
            if row['DEP'] not in ['101', '102', '103', '104']:
                return row['COM']
            first_digit = str(digit_mapping.get(row['DEP']))
            return first_digit + row['COM'][1:]
        data['COM'] = data.apply(convert_city, axis=1)

        baseurl = "%s/communes/eneuro/detail.php?icom=%%(COM)s&dep=%%(DEP)s&type=BPS&param=0&exercice=%s"%(self.domain,str(year))
        return [baseurl%row for __, row in data.iterrows()]

    def parse(self, response):
        if "/communes/eneuro/detail_gf.php" in response.url:
            return self.parse_epci(response)
        elif "/communes/eneuro/detail.php" in response.url:
            return self.parse_commune(response)
        elif "/departements/detail.php" in response.url or \
                "/regions/detail.php" in reponse.url:
            self.parse_dep_and_reg(response)

    def parse_commune(self, response):
        """Parse the response and return an Account object"""
        hxs = HtmlXPathSelector(response)
        icom, dep, year = re.search('icom=(\d{3})&dep=(\w{3})&type=\w{3}&param=0&exercice=(\d{4})', response.url).groups()
        try:
            data = parse_city_page_account(icom, dep, year, response)
            # convert account object to an Item instance.
            # WHY DO I NEED TO DO THAT SCRAPY ????
            item = CityFinancialData(data)
            return item
        except:
            data = {'code': icom+dep, 'year': year, 'is_city': True, 'url': response.url}
            log.msg('failed url %s'%response.url, level=log.ERROR)
            raise

    def parse_epci(self, response):
        hxs = HtmlXPathSelector(response)

    def parse_dep_and_reg(self, response):
        hxs = HtmlXPathSelector(response)


