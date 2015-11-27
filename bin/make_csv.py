# -*- coding: utf-8 -*-

import os
import sys
import json
import re
import codecs

from unicodecsv import DictWriter
from collections import defaultdict

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(PROJ_DIR)
from localfinance.parsing.document_mapper import DocumentMapper

MAPPING_FILES = os.listdir('data/mapping')


def get_all_variables_by_locality():
    variables = defaultdict(set)

    for mapping_file in MAPPING_FILES:
        locality = re.match('(\w+)_\d{4}\.yaml', mapping_file).groups()[0]
        variables[locality] = variables[locality].union(DocumentMapper(os.path.join(PROJ_DIR, 'data', 'mapping', mapping_file)).get_all_fields())

    return variables


def make_csv():
    data_files = os.listdir('scraped_data')
    fieldnames_by_locality = get_all_variables_by_locality()

    for zone_type in ['city', 'department', 'epci', 'city']:
        locality_data_files = [data_file for data_file in data_files if zone_type in data_file]

        fieldnames = ['year', 'zone_type', 'name', 'population', 'insee_code', 'url'] + sorted(list(fieldnames_by_locality[zone_type]))

        if zone_type == 'epci':
            fieldnames.append('siren')

        with open(os.path.join('nosdonnees', zone_type + '_all.csv'), 'w') as output:
            csv_output = DictWriter(output, fieldnames=fieldnames, encoding='utf-8')

            for locality_data_file in locality_data_files:
                print locality_data_file
                with codecs.open(os.path.join('scraped_data', locality_data_file), encoding='utf-8') as input:
                    for line in input:
                        data = json.loads(line, encoding='utf-8')['data']
                        csv_output.writerow(data)

make_csv()

mapping = {
    'name': u'Nom',
    'year': u'Année',
    'zone_type': u'Type de zone administrative',
    'population': u'Population',
    'insee_code': u'Code Officiel Géographique (insee)'
}
