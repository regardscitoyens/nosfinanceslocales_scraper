# -*- coding: utf-8 -*-

import re

from ..utils import clean_name
from ..utils import sanitize_value


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
                    print "Entering in section %s" % section
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


class DepartmentFinance2013Parser(DepartmentFinanceParser):
    finance_value_icol = 0
    finance_name_icol = 3


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
