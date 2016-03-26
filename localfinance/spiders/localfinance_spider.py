# -*- coding: utf-8 -*-

import re

import pandas as pd
from scrapy.spiders import Spider
from scrapy.selector import Selector

from ..parsing.zone import (
    CityZoneParser,
    EPCIZoneParser,
    DepartmentZoneParser,
    RegionZoneParser
)
from ..item import LocalFinance
from ..utils import DOM_DEP_MAPPING, uniformize_code, convert_dom_code, get_dep_code_from_com_code, convert_city


class LocalFinanceSpider(Spider):
    """Basic spider which crawls all pages of finance of french towns, departments
    regions and EPCI.
    """
    name = "localfinance"
    domain = "http://alize2.finances.gouv.fr"
    allowed_domains = [domain]

    def __init__(self, year=2014, zone_type='city'):
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
        insee_code_file = "data/locality/depts2013.txt"
        data = pd.io.parsers.read_csv(insee_code_file, '\t')
        data['DEP'] = uniformize_code(data, 'DEP')
        data['DEP'] = convert_dom_code(data)
        baseurl = "%s/departements/detail.php?dep=%%(DEP)s&exercice=%s" % (self.domain, year)
        return [baseurl % row for __, row in data.iterrows()]

    def get_reg_urls(self, year):
        insee_code_file = "data/locality/reg2013.txt"
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
        baseurl = "%s/regions/detail.php?reg=%%(REGION)s&exercice=%s" % (self.domain, year)
        return [baseurl % row for __, row in data.iterrows()]

    def get_epci_urls(self, year):
        data = pd.read_csv('data/locality/epci.csv')
        base_url = "%s/communes/eneuro/detail_gfp.php?siren=%%(siren)s&dep=%%(dep)s&type=BPS&exercice=%s" % (self.domain, str(year))

        return [base_url % row for __, row in data.iterrows()]

    def get_commune_urls(self, year):
        """
        The communes pages urls depends on 5 parameters:
        - COM: the insee code of the commune
        - DEP: the department code on 3 characters
        - type: type of financial data, BPS is for the whole data.
        - exercise: year of financial data
        """

        insee_code_file = "data/locality/france2013.txt"
        data = pd.io.parsers.read_csv(insee_code_file, '\t')

        # XXX: insee_communes file contains also "cantons", filter out these lines
        mask = data['ACTUAL'].apply(lambda v: v in [1, 2, 3])
        data = data[mask].reindex()

        # XXX: as always paris is the exception. City code is 101 for years < 2010 and 056 for years >= 2010
        # 056 is the right code, add 101 also to crawl pages for years < 2010
        paris_row = data[(data.COM == 56) & (data.DEP == '75')].copy()
        paris_row.COM = 101
        data = data.append(paris_row)

        data['DEP'] = uniformize_code(data, 'DEP')
        data['COM'] = uniformize_code(data, 'COM')

        data['DEP'] = convert_dom_code(data)

        data['COM'] = data.apply(convert_city, axis=1)

        base_url = "%s/communes/eneuro/detail.php?icom=%%(COM)s&dep=%%(DEP)s&type=BPS&param=0&exercice=%s" % (self.domain, str(year))

        return [base_url % row for __, row in data.iterrows()]

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
        hxs = Selector(response)

        h3_strings = hxs.xpath("//body/h3/text()").extract()

        if h3_strings and h3_strings[0].startswith("Aucune commune"):
            return []

        icom, dep, year = re.search('icom=(\d{3})&dep=(\w{3})&type=\w{3}&param=0&exercice=(\d{4})', response.url).groups()

        # XXX: better to use the real insee code for later analysis, not icom and dep in url.
        real_dep = dict([(val, key) for key, val in DOM_DEP_MAPPING.items()]).get(dep, dep[1:])
        real_com = icom if dep not in DOM_DEP_MAPPING.values() else icom[1:]
        real_insee_code = real_dep + real_com

        # XXX: hack for paris ! \o/
        if real_insee_code == '75101':
            real_insee_code = '75056'

        data = CityZoneParser(real_insee_code, year, response.url).parse(hxs)
        return LocalFinance(id=real_insee_code, data=data)

    def parse_epci(self, response):
        hxs = Selector(response)
        siren, year = re.search('siren=(\d+)&dep=\w{3}&type=BPS&exercice=(\d{4})', response.url).groups()

        if 'Aucun GFP correspondant' in response.body:
            self.logger.warning("No epci for siren=%s and year=%s (%s)" % (siren, year, response.url))
            return

        data = EPCIZoneParser("", year, response.url, siren).parse(hxs)
        return LocalFinance(id=siren, data=data)

    def parse_dep(self, response):
        hxs = Selector(response)

        h3_strings = hxs.xpath("//body/h3/text()").extract()

        if h3_strings and h3_strings[0].startswith(u'Aucune donn\xe9es'):
            return []

        dep, year = re.search('dep=(\w{3})&exercice=(\d{4})', response.url).groups()

        data = DepartmentZoneParser(dep, year, response.url).parse(hxs)
        return LocalFinance(id=dep, data=data)

    def parse_reg(self, response):
        hxs = Selector(response)

        h3_strings = hxs.xpath("//body/h3/text()").extract()

        if h3_strings and h3_strings[0].startswith(u'Aucune donn\xe9es'):
            return []

        dep, year = re.search('reg=(\w{3})&exercice=(\d{4})', response.url).groups()

        data = RegionZoneParser(dep, year, response.url).parse(hxs)
        return LocalFinance(id=dep, data=data)