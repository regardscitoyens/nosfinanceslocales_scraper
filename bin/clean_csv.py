# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.path.abspath('.'))
import pandas as pd

from localfinance.account_network import (
    city_account,
    region_account,
    department_account,
    city_account,
    epci_account
)

csvfile = sys.argv[1]
zone_type = sys.argv[2]

# dir where we put data for nosdonnees.fr
csvoutput = os.path.join('nosdonnees', os.path.basename(csvfile))

df = pd.read_csv(csvfile)
df = df.dropna(axis=1, how='all')
if zone_type == 'region':
    account = region_account
elif zone_type == 'department':
    account = department_account
elif zone_type == 'epci':
    account = epci_account
elif zone_type == 'city':
    account = city_account
else:
    print "Define a zone_type"
    raise

mapping = {
    'name': u'Nom',
    'year': u'Année',
    'zone_type': u'Type de zone administrative',
    'population': u'Population',
    'insee_code': u'Code Officiel Géographique (insee)'
}
def get_fr_name(column):
    node = account.nodes.get(column)
    if node:
        names = node['name']
        if type(names) in [unicode, str]:
            return names
        else:
            return names[0]
    else:
        return mapping.get(column, column)

fr_columns = []
for column in df.columns.tolist():
    fr_name = get_fr_name(column).lower()
    fr_columns.append(fr_name)
    df[fr_name] = df[column]

outputdf = df[sorted(fr_columns)]
outputdf.to_csv(csvoutput, index=False, encoding='utf-8')

