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
        for key, value in self.mapping['tax']['types'].items():
            s = SequenceMatcher(None, name.lower(), value.lower())
            if s.ratio() > 0.5:
                taxes.append((s.ratio(), key))
        return sorted(taxes)[-1][1] if taxes else []

    def is_section(self, name):
        return name.strip().lower() in self.sections
