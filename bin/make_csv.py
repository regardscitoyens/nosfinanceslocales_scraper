# -*- coding: utf-8 -*-

import os
import sys
import json
import codecs

from unicodecsv import DictWriter

PROJ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJ_DIR)

from localfinance.utils import get_all_variables_by_locality


MAPPING_FILES = os.listdir('data/mapping')


def make_csv():
    data_files = os.listdir('scraped_data')
    fieldnames_by_locality = get_all_variables_by_locality()

    for zone_type in ['epci']:
        print "Make %s csv..." % zone_type

        locality_data_files = [data_file for data_file in data_files if zone_type in data_file]

        variables_mapping = {
            'name': u'nom',
            'year': u'année',
            'zone_type': u'type de zone administrative',
            'population': u'population',
            'insee_code': u'cog (code officiel géographique)',
            'url': u'url'
        }

        fieldnames = ['year', 'zone_type', 'name', 'population', 'insee_code', 'url'] \
            + sorted(fieldnames_by_locality[zone_type].keys())

        variables_mapping.update(fieldnames_by_locality[zone_type])

        if zone_type == 'epci':
            fieldnames.append('siren')

        with open(os.path.join('nosdonnees', zone_type + '_all.csv'), 'w') as output:
            csv_output = DictWriter(output, fieldnames=fieldnames, encoding='utf-8')

            csv_output.writerow(variables_mapping)

            for locality_data_file in locality_data_files:
                with codecs.open(os.path.join('scraped_data', locality_data_file), encoding='utf-8') as input:
                    for line in input:
                        data = json.loads(line, encoding='utf-8')['data']
                        csv_output.writerow(data)


make_csv()