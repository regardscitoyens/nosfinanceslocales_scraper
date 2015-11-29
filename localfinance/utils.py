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