# -*- coding: utf-8 -*-

import re


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

