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
    allowed_domains = ["http://alize2.finances.gouv.fr"]

    def __init__(self, insee_code_file="./data/france2013.txt", year=2012):
        """Load insee code of every commune in france and generate all the urls to
        crawl."""

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
        # Finally, DOM cities have an insee_code on 2 digits in the insee file. We need
        # to add a third digit before these two to crawl the right page.
        def convert_city(row):
            if row['DEP'] in ['101', '102', '103', '104']:
                return row['DEP'][-1] + row['COM'][1:]
            else:
                return row['COM']
        data['COM'] = data.apply(convert_city, axis=1)

        baseurl = "http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom=%(COM)s&dep=%(DEP)s&type=BPS&param=0&exercice=" + str(year)
        self.start_urls = [baseurl%row for __, row in data.iterrows()]

    def parse(self, response):
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


