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
        xls = pd.ExcelFile('.cache/epci-au-01-01-%s.xls' % year)
        sheet = xls.parse('Composition communale des EPCI')
        sheet['siren'] = sheet[u'Établissement public à fiscalité propre'][1:]
        sheet['dep'] = sheet[u'Département commune'].apply(get_dep_code_from_com_code)
        data = sheet.groupby(['siren', 'dep'], as_index=False).first()[['siren', 'dep']]

        if all_data is None:
            all_data = data
        else:
            all_data = all_data.append(data)


    all_data.drop_duplicates().to_csv('data/locality/epci.csv', index=False, encoding='utf-8')


make_epci_csv()