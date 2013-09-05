# -*- coding: utf-8 -*-
import re
from collections import defaultdict

from scrapy.selector import HtmlXPathSelector

from .account_network import city_account

def parse_city_page_account(icom, dep, year, response):
    """Parse html account table of a city for a given year
    crawled from http://alize2.finances.gouv.fr.
    Return an account instance which gathers all parsed data."""

    hxs = HtmlXPathSelector(response)

    # select tables of interest
    table1 = hxs.select('.//table')[2]

    # In the first table, the second row gives the name of the city
    trs = table1.select('.//tr')
    name = trs[1].select('.//td/text()')[1].extract()

    # the third row gives the population
    population = trs[2].select('.//th/text()')[1].extract()
    print population
    population = re.search(r':([\d\s]+)', population).groups()[0]
    population = int(population.replace(' ', ''))

    scraped_data = {
        'insee_code': dep+icom,
        'year': year,
        'name': name,
        'zone_type': 'city',
        'population': population,
    }

    scraped_data.update(parse_city_table_1(table1))

    # For years > 2008, we have two tables with data
    if int(year) > 2008:
        table2 = hxs.select('.//table')[5]
        scraped_data.update(parse_city_table_2(table2))

    return scraped_data

def parse_city_table_1(table):
    # For this table, we have:
    # - the value is always in the first column of the table. If there is no value,
    # this is just section of the account of the city.
    # - the name of the row is defined the third column.

    icol_value = 0
    icol_value_per_person = 1
    icol_name = 3

    scraped_data = {}

    for tr in table.select('.//tr')[5:]:
        tds = tr.select('.//td/text()')
        if len(tds) < 5:
            continue
        # Don't forget to remove whitespace in ascii ?
        value = convert_value(tds[icol_value].extract()) * 1000
        str_value_per_person = tds[icol_value_per_person].extract()
        value_per_person = convert_value(str_value_per_person)
        # Strip line and remove "dont" keyword.
        name = tds[icol_name].extract().replace('dont :', '').strip()

        # We are only interested in accountline
        node_type = 'accountline'

        targets = city_account.find_node(name=name, type=node_type)
        if targets:
            target = targets[0]
            if value is not None and value_per_person is not None:
                scraped_data[target] = value
        else:
            print "There is no node of name %s and type %s"%(name, node_type)

    return scraped_data

def parse_city_table_2(table):
    # This table contains info about taxes. The format of the table is very annoying.
    # => all the code written here is very specific to this format and will crash as
    # soon as a slight change of the html will occur.
    # XXX: This parsing is just a horrible shit
    # TODO: erase this fucking crappy code, make this parsing acceptable.
    scraped_data = defaultdict(dict)
    irow_start_1 = 4
    irow_start_2 = 10
    irow_start_3 = 17
    nb_rows = 5
    nb_rows_3 = 3
    rows = table.select('.//tr')
    attr_name = 'basis'
    parse_tablepart(rows[irow_start_1:irow_start_1+nb_rows], attr_name, 0, scraped_data)
    attr_name = 'cuts_on_deliberation'
    parse_tablepart(rows[irow_start_1:irow_start_1+nb_rows], attr_name, 4, scraped_data)
    attr_name = 'value'
    parse_tablepart(rows[irow_start_2:irow_start_2+nb_rows], attr_name, 0, scraped_data)
    attr_name = 'voted_rate'
    parse_tablepart(rows[irow_start_2:irow_start_2+nb_rows], attr_name, 4, scraped_data)

    parse_tablepart(rows[irow_start_3:irow_start_3+nb_rows_3], attr_name, 4, scraped_data)
    attr_name = 'value'
    parse_tablepart(rows[irow_start_3:irow_start_3+nb_rows_3], attr_name, 0, scraped_data)

    return scraped_data

def parse_tablepart(rows, attr_name, icol, scraped_data):
    # Attempt to factorize some code... but failed to reach an acceptable code.
    # XXX: erase all this crap.
    icol_name = 3
    for row in rows:
        tds = row.select('.//td/text()')
        if len(tds) < 6:
            continue
        name = tds[icol_name].extract().strip()
        targets = city_account.find_node(name=name, type='accountline')
        if targets:
            target = targets[0]
            str_val = tds[icol].extract()
            val = convert_value(str_val)
            if attr_name <> 'voted_rate':
                val = val * 1000 if val else None

            scraped_data[target][attr_name] = val

            if icol <> 0 and len(tds) == 7:
                scraped_data[target][attr_name] = convert_value(tds[icol+1].extract())

    return scraped_data

def convert_value(val):
    val = val.replace(u'\xa0', '')\
             .replace(',', '.')\
             .replace('-', '')\
             .replace(u'\xa0', '')\
             .replace(' ', '')
    if val:
        if '%' in val:
            val = float(val.replace('%', ''))/100
        return float(val)
    else:
        return None



