# -*- coding: utf-8 -*-

import pandas as pd
import re

from scrapy import log
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field

from localgouv.account_parsing import parse_city_page_account

class AccountData(Item):
    data = Field()

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

    def __init__(self, insee_code_file="./data/insee_communes.txt", year=2012):
        """Load insee code of every commune in france and generate all the urls to
        crawl."""
        data = pd.io.parsers.read_csv(insee_code_file, '\t')
        def uniformize_dep_code(dep_code):
            return dep_code if len(dep_code) == 3 else "0%s"%dep_code
        data['DEP'] = data['DEP'].apply(uniformize_dep_code)
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
            item = AccountData(data=data)
            return item
        except:
            data = {'code': icom+dep, 'year': year, 'is_city': True, 'url': response.url}
            log.msg('failed url %s'%response.url, level=log.ERROR)
            raise


