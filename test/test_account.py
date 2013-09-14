# -*- coding: utf-8 -*-

import sys
import unittest2

from unipath import Path
sys.path.append(Path(__file__).ancestor(2))

from localgouv.account_network import Account, make_city_account

class AccountTestCase(unittest2.TestCase):
    def test_account(self):
        """Just test the instanciation"""
        account = Account()
        account.add_line('localtax', name=u'Impôts Locaux')
        account.add_line('other_tax', name=u'Autres impôts et taxes')
        account.add_line('allocation', name=u'Dotation globale de fonctionnement')
        account.add_section('operating_revenues_A', name=u'TOTAL DES PRODUITS DE FONCTIONNEMENT = A')
        account.add_edges('operating_revenues_A', ['localtax', 'other_tax', 'allocation'])

    def test_town_account(self):
        account = make_city_account()
        self.assertEqual(85, len(account.nodes.items()))

    def test_find(self):
        account = Account()
        account.add_line('localtax', name=u'Impôts Locaux', other=u'test')
        account.add_line('localtax2', name=u'Impôts Locaux', other=u'test2')
        self.assertEqual(len(account.find_node(**{'name': u'Impôts Locaux'})), 2)
        self.assertEqual(len(account.find_node(**{'name': u'Impôts Locaux',
                                                  'other':u'test2'})), 1)

    def test_root(self):
        account = make_city_account()
        self.assertEqual(account.root, 'root')

if __name__ == '__main__':
    unittest2.main()

