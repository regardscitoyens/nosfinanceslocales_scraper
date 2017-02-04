# -*- coding: utf-8 -*-

import os
import sys

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJ_DIR)

import pandas as pd
from localfinance.utils import get_dep_code_from_com_code


def make_epci_csv():

    all_data = None

    for year in range(2012, 2015):
        data = pd.read_csv('.cache/epcicom%s.csv' % year, delimiter=";", encoding="iso-8859-1")
        data['siren'] = data['siren_epci']
        data['dep'] = data['dep_epci'].apply(get_dep_code_from_com_code)
        if all_data is None:
            all_data = data
        else:
            all_data = all_data.append(data)

    all_data[['siren', 'dep']].drop_duplicates().to_csv('data/locality/epci.csv', index=False, encoding='utf-8')


make_epci_csv()