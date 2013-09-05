# -*- coding: utf-8 -*-

class Network(object):
    """Directed graph. Mainly taken from networkx lib, but simplified for the usage"""
    def __init__(self, **attr):
        self.metadata = attr or {}
        self.nodes = {}
        self.succ = {}
        self.pred = {}

    def init_node(self, node, attr=None):
        self.nodes[node] = attr or {}
        self.succ[node] = {}
        self.pred[node] = {}

    @property
    def root(self):
        return [node for node, attr in self.pred.iteritems() if not attr][0]

    def add_node(self, node, **attr):
        self.init_node(node, attr)

    def add_edge(self, node1, node2, **attr):
        if node1 not in self.nodes:
            self.init_node(node1)
        if node2 not in self.nodes:
            self.init_node(node2)

        self.succ[node1][node2] = attr or {}
        self.pred[node2][node1] = attr or {}

    def add_edges(self, source, nodes, attrs=None):
        attrs = attrs or {}
        for node in nodes:
            self.add_edge(source, node, **attrs.get(node, {}))

    def successors(self, node):
        return list(self.succ[node].keys())

    def predecessors(self, node):
        return list(self.pred[node].keys())

    def find_node(self, **attr):
        """Find a node by its attributes"""
        matched_nodes = []
        for node, node_attr in self.nodes.iteritems():
            append = True
            for attr_k, attr_v in attr.iteritems():
                values = node_attr.get(attr_k)
                if type(values) in [list, tuple]:
                    append = False
                    for value in values:
                        if attr_v in value:
                            append = True
                else:
                    if attr_v not in values:
                        append = False
                if not append:
                    break
            if append:
                matched_nodes.append(node)

        return matched_nodes

    def find_nearest_node(self, source, attr):
        raise NotImplementedError

    def descendants(self, node):
        raise NotImplementedError

    def ancestors(self, node):
        raise NotImplementedError

class Account(Network):
    """A city/group of cities/department/region account: it is described as a
    directed graph made of account lines and sections regrouping others lines and
    sections.
    TODO: add edge rules which ensure the relationship between account lines:
        for example, an account line can be the sum of its children.
    """
    def add_line(self, node, **attr):
        attr = attr or {}
        attr.update(type="accountline")
        self.add_node(node, **attr)

    def add_section(self, node, **attr):
        attr = attr or {}
        attr.update(type="section")
        self.add_node(node, **attr)

    def add_relationship(self, node, r_nodes, operator):
        raise NotImplementedError

    def iterlines(self):
        for k, v in self.nodes.iteritems():
            if 'type' in v and v['type'] == 'accountline':
                yield (k, v)

def make_city_account():
    """Create city's account: note that there are little differences between fiscal
    years...
    All is based on info from http://www.collectivites-locales.gouv.fr/"""

    account = Account()
    account.add_section('root')

    # OPERATINGS OPERATIONS
    ## REVENUES
    account.add_line('localtax', name=u'Impôts Locaux')
    account.add_line('other_tax', name=u'Autres impôts et taxes')
    account.add_line('allocation', name=u'Dotation globale de fonctionnement')
    account.add_line('operating_revenues', name=u'TOTAL DES PRODUITS DE FONCTIONNEMENT = A')
    account.add_edges('operating_revenues', ['localtax', 'other_tax', 'allocation'])

    ## EXPENSES
    account.add_line('staff_costs', name=u'Charges de personnel')
    account.add_line('purchases_and_external_costs', name=u'Achats et charges externes')
    account.add_line('financial_costs', name=u'Charges financières')
    account.add_line('contigents', name=u'Contingents') # Find another name ?
    account.add_line('paid_subsidies', name=u'Subventions versées')
    account.add_line('operating_costs', name=u'TOTAL DES CHARGES DE FONCTIONNEMENT = B')
    account.add_edges('operating_costs', ['staff_costs', 'purchases_and_external_costs',
                                          'financial_costs', 'contigents',
                                          'paid_subsidies'])
    # PROFIT
    account.add_line('net_profit', name=u'RESULTAT COMPTABLE = A - B = R')
    account.add_edge('root', 'net_profit')

    account.add_line('operatings_operations', name=u'OPERATIONS DE FONCTIONNEMENT')
    account.add_edges('operatings_operations', ['operating_revenues', 'operating_costs'])
    account.add_edge('root', 'operatings_operations')

    # INVESTMENTS OPERATIONS
    account.add_section('investments', name="OPERATIONS D'INVESTISSEMENT")
    account.add_edge('root', 'investments')
    ## INVESTMENTS RESSOURCES
    account.add_line('loans', name=u"Emprunts bancaires et dettes assimilées")
    account.add_line('received_subsidies', name=u"Subventions reçues")
    account.add_line('fctva', name=u"FCTVA") # What is FCTVA ?
    account.add_line('returned_properties', name=u"Retour de biens affectés, concédés, ...")
    account.add_line('investment_ressources', name=u"TOTAL DES RESSOURCES D'INVESTISSEMENT = C")
    account.add_edges('investment_ressources', ['loans', 'received_subsidies',
                                                'fctva', 'returned_properties'])

    ## INVESTMENTS USAGE
    account.add_line('facilities_expenses', name=u"Dépenses d'équipement")
    account.add_line('debt_repayments', name=u"Remboursement d'emprunts et dettes assimilées")
    account.add_line('costs_to_allocate', name=u"Charges à répartir")
    account.add_line('fixed_assets', name=u"Immobilisations affectées, concédées, ...")
    account.add_line('investments_usage', name=u"TOTAL DES EMPLOIS D'INVESTISSEMENT = D")
    account.add_edges('investments_usage', ['facilities_expenses', 'debt_repayments',
                                            'costs_to_allocate', 'fixed_assets'])

    account.add_edges('investments', ['investment_ressources', 'investments_usage'])

    ## SELF-FINANCING
    account.add_section('self_financing', name=u'AUTOFINANCEMENT')
    account.add_edge('root', 'self_financing')
    account.add_line('surplus', name=u'Excédent brut de fonctionnement')
    account.add_line('self_financing_capacity', name=u"Capacité d'autofinancement = CAF")
    account.add_line('debt_repayment_capacity', name=u"CAF nette du remboursement en capital des emprunts")
    account.add_edges('self_financing', ['surplus', 'self_financing_capacity',
                                         'debt_repayment_capacity'])

    ## LIABILITIES
    account.add_section('liabilities', name=u'ENDETTEMENT')
    account.add_edge('liabilities', 'self_financing')
    account.add_edge('root', 'liabilities')
    account.add_line('debt_at_end_year', name=u'Encours total de la dette au 31/12/N')
    account.add_line('debt_annual_costs', name=u'Annuité de la dette')
    account.add_line('advances_from_treasury', name=u'Avances du Trésor au 31/12/N')
    account.add_edges('liabilities', ['debt_at_end_year', 'debt_annual_costs',
                                      'advances_from_treasury'])

    # TAXES
    account.add_section('taxation', name=u'ELEMENTS DE FISCALITE DIRECTE LOCALE')
    account.add_edge('root', 'taxation')
    account.add_line('home_tax', name=[u"Taxe d'habitation (y compris THLV)",
                                       u"Produits taxe d'habitation"])
    account.add_line('property_tax', name=[u"Taxe foncière sur les propriétés bâties",
                                           u"Produits foncier bâti"])
    account.add_line('land_property_tax', name=[u"Taxe foncière sur les propriétés non bâties", u"Produits foncier non bâti"])
    account.add_line('compensation_2010', name=u"Compensation-Relais 2010")
    account.add_line('business_tax', name=[u"Taxe professionnelle (hors produits écrêtés)",
                                           u"Taxe professionnelle (hors bases écrêtées)",
                                           u"Produits taxe professionnelle"])
    account.add_line('additionnal_land_property_tax', name=u"Taxe additionnelle à la taxe foncière sur les propriétés non bâties")
    account.add_line('business_property_contribution', name=u'Cotisation foncière des entreprises')
    account.add_edges('taxation', ['home_tax', 'property_tax', 'land_property_tax',
                                   'additionnal_land_property_tax', 'compensation_2010',
                                   'business_tax', 'business_property_contribution'])

    ## TAX REVENUES
    account.add_section('allocation_tax_revenues', name=u'Les produits des impôts de répartition')
    account.add_edge('taxation', 'allocation_tax_revenues')
    account.add_line('business_profit_contribution', name=u'Cotisation sur la valeur ajoutée des entreprises')
    account.add_line('business_network_tax', name=u'Impositions forfaitaires sur les entreprises de réseau')
    account.add_line('retail_land_tax', name=u'Taxe sur les surfaces commerciales')
    account.add_edges('allocation_tax_revenues', ['business_profit_contribution',
                                                  'business_network_tax',
                                                  'retail_land_tax'])

    account.add_edges('taxation', ['home_tax', 'property_tax', 'land_property_tax',
                                   'additionnal_land_property_tax',
                                   'allocation_tax_revenues'])

    return account

city_account = make_city_account()
