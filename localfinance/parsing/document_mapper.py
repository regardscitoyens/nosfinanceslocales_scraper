# -*- coding: utf-8 -*-

import yaml
import codecs

from difflib import SequenceMatcher


class DocumentMapper(object):
    def __init__(self, yaml_file):
        self.mapping = yaml.load(codecs.open(yaml_file, 'r', encoding="utf-8"))
        self.sections = [s.strip().lower() for s in self.mapping.keys()]

    def find_node(self, section, name):
        if not section or section not in self.mapping:
            return None

        for key, value in self.mapping[section].items():
            if name.lower() in value.lower():
                return key

    def find_tax(self, name):
        taxes = []
        for key, value in self.mapping['tax'].items():
            s = SequenceMatcher(None, name.lower(), value.lower())
            if s.ratio() > 0.5:
                taxes.append((s.ratio(), key))
        return sorted(taxes)[-1][1] if taxes else []

    def is_section(self, name):
        return name.strip().lower() in self.sections

    def get_all_fields(self):
        fields = {}
        tax_field_keys = ['rate', 'value', 'basis', 'cuts_on_deliberation']
        tax_field_names = [u'taux', u'produits', u'base nette imposée', u'réductions de bases accordées sur délibérations']
        for section, values in self.mapping.items():
            for item in values.items():
                if section == 'tax':
                    for tax_field_key, tax_field_name in zip(tax_field_keys, tax_field_names):
                        key = item[0] + '_' + tax_field_key
                        name = item[1] + ' - ' + tax_field_name
                        fields.update({key: name.lower()})
                else:
                    fields.update({item[0]: item[1].lower()})
        return fields
