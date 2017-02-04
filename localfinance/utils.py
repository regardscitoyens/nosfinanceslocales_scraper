# -*- coding: utf-8 -*-

import os
import re
from collections import defaultdict
from localfinance.parsing.document_mapper import DocumentMapper


def sanitize_value(val):
    """Remove crap from val string and then convert it into float"""
    val = re.sub(u"(\xa0|\s)", '', val)
    val = val.replace(',', '.')

    # positive or negative multiplier
    mult = 1

    if '-' in val and len(val) > 1:
        mult = -1
        val = val.replace('-', '')
    elif '-' in val:
        val = '0'

    if val is not None:
        if '%' in val:
            val = float(val.replace('%', ''))
        return float(val) * mult


def clean_name(name):
    return re.sub("(dont|\:|\+)", "", name).strip()


def get_all_variables_by_locality():
    variables = defaultdict(dict)

    mapping_dir = 'data/mapping'

    for mapping_file in os.listdir(mapping_dir):
        locality = re.match('(\w+)_\d{4}\.yaml', mapping_file).groups()[0]
        variables[locality].update(DocumentMapper(os.path.join(mapping_dir, mapping_file)).get_all_fields())

    return variables


def uniformize_code(df, column):
    # Uniformize dep code and commune code to be on a string of length 3.
    def _uniformize_code(code):
        return ("00%s" % code)[-3:]

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
    com = com.zfill(3)
    return DOM_DEP_MAPPING.get(com, com)

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

