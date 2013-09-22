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

    def add_nodes(self, nodes):
        for node, attr in nodes.items():
            self.add_node(node, **attr)

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
                node_attr_v = node_attr[attr_k] if attr_k in node_attr else None
                if attr_k in node_attr and (attr_v == node_attr_v or attr_v in node_attr_v):
                    pass
                else:
                    append = False
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
    def add_section(self, node, **attr):
        attr = attr or {}
        attr.update(type="section")
        self.add_node(node, **attr)

    def add_relationship(self, node, r_nodes, operator):
        raise NotImplementedError

# TODO: use lower case to compare

def add_operating_operations(account):
    """Operating nodes"""
    account.add_nodes({
        'operatings_operations': {'name': u'OPERATIONS DE FONCTIONNEMENT', 'type': 'section'},
        'operating_revenues': {'name': [u'TOTAL DES PRODUITS DE FONCTIONNEMENT = A', u"Total des produits de fonctionnement = A"]},
        'other_tax': {'name': u"Autres impôts et taxes"},
        'allocation': {'name': [u'Dotation globale de fonctionnement',
                                u'dotation globale de fonctionnement']},
        'operating_costs': {'name': [u"Total des charges de fonctionnement = B", u'TOTAL DES CHARGES DE FONCTIONNEMENT = B']},
        'staff_costs': {'name': [u'Charge de personnel (montant net)', u'Charges de personnel']},
        'purchases_and_external_costs': {'name': u'Achats et charges externes (montant net)'},
        'financial_costs': {'name': u'Charges financières'},
        'net_profit': {'name': [u"Résultat comptable = A - B", u'RESULTAT COMPTABLE = A - B = R']},
    })

    account.add_edge('root', 'operatings_operations')
    account.add_edges('operatings_operations', ['net_profit', 'operating_revenues', 'operating_costs'])

    account.add_edges('operating_revenues', ['other_tax', 'allocation'])

    account.add_edges('operating_costs',
                      ['staff_costs', 'purchases_and_external_costs',
                       'financial_costs'])

def add_investments_operations(account):
    account.add_nodes({
        'investments': {'name': u"OPERATIONS D'INVESTISSEMENT", 'type': 'section'},
        'investment_ressources': {
            'name': [u"TOTAL DES RESSOURCES D'INVESTISSEMENT = C",
                      u"Total des ressources d'investissement budgétaires = C"]
        },
        'fctva': {'name': u"FCTVA"},
        'received_subsidies': {
            'name': [u"Subventions d'investissements reçues", u"Subventions reçues"]
        },
        'loans': {'name': [u"Emprunts souscrits",
                           u"Emprunts bancaires et dettes assimilées"]},
        'investments_usage': {
            'name': [u"Total des emplois d'investissement budgétaires = D",
                      u"TOTAL DES EMPLOIS D'INVESTISSEMENT = D"]
        },
        'debt_repayments': {
            'name': [u"Remboursement en capital des emprunts",
                     u"Remboursement d'emprunts et dettes assimilées"]
        },
        'residual_financing_capacity': {
            'name': [u"Besoin de financement résiduel = D-C",
                     u"Besoin ou capacité de financement Résiduel de la section d'investissement = D - C"]
        },
        'thirdparty_balance': {'name': [u"Solde des opérations pour compte de tiers",
                                        u"Solde des opérations pour le compte de tiers"]},
        'financing_capacity': {
            'name': [u"Besoin de financement de la section d'investissement",
                     u"= Besoin ou capacité de financement de la section d'investissement = E"]
        },
        'global_profit': {'name': [u"Résultat d'ensemble", u"Résultat d'ensemble = R - E"]},
    })

    account.add_edges('root', ['investments', 'global_profit'])
    account.add_edges('investments', ['investment_ressources', 'fctva', 'loans',
                                      'received_subsidies', 'investments_usage',
                                      'debt_repayments', 'thirdparty_balance',
                                      'financing_capacity'])

def add_debt(account):
    account.add_nodes({
        'liabilities': {'name': 'ENDETTEMENT', 'type': 'section'},
        'debt_at_end_year': {'name': [u'encours des dettes bancaires et assimilées', u"Encours total de la dette au 31/12/N"]},
        'debt_annual_costs': {'name': [u'Annuité de la dette', u"Annuité des dettes bancaires et assimilées"]},
    })
    account.add_edge('root', 'liabilities')
    account.add_edges('liabilities', ['debt_at_end_year', 'debt_annual_costs'])
    return account

def add_tax_infos(account, taxes):
    tax_infos = {'basis': u"Bases nettes imposées",
                 'cuts_on_deliberation': u"Réductions de bases accordées sur délibérations",
                 'value': u"Produits des impôts locaux",
                 'rate': u"Taux voté"}

    for tax in taxes:
        for (tax_info, tax_info_name) in tax_infos.items():
            tax_info_node = "%s_%s"%(tax, tax_info)
            node_name = account.nodes[tax]['name']
            node_name = node_name if type(node_name) in [str, unicode] \
                                  else node_name[0]
            account.add_node(tax_info_node, name="%s de la %s"%(tax_info_name, node_name))
            account.add_edge(tax, tax_info_node)


def add_taxation(account):
    account.add_nodes({
        'taxation': {'name': u'ELEMENTS DE FISCALITE LOCALE', 'type': 'section'},
        'business_tax': {
            'name': [u"Taxe professionnelle",
                     u"Taxe professionnelle (hors produits écrêtés)",
                     u"Taxe professionnelle (hors bases écrêtées)",
                     u"Produits taxe professionnelle",
                     u"Taxe professionnelle (",
                     u'Taxe professionnelle (fiscalité additionnelle)'],
            'type': 'section'
        },
        'business_profit_contribution': {
            'name': [u'Cotisation sur la valeur ajoutée des entreprises',
                     u'Cotisation Valeur Ajoutée des Entreprises'],
            'type': 'section'
        },
        'business_network_tax': {
            'name': [u'Impositions forfaitaires sur les entreprises de réseau',
                     u'Imposition forfaitaire sur les entreprises de réseau'],
            'type': 'section'
        },
        'property_tax': {
            'name': [u"Taxe foncière sur les propriétés bâties",
                     u"Produits foncier bâti"],
            'type': 'section'
        },
        'land_property_tax': {
            'name': [u"Taxe foncière sur les propriétés non bâties",
                    u"Produits foncier non bâti"],
            'type': 'section'
        },
    })

    account.add_edge('root', 'taxation')
    account.add_edges('taxation', ['business_tax', 'business_profit_contribution',
                                   'business_network_tax', 'property_tax',
                                   'land_property_tax'])
    add_tax_infos(account, ['business_tax', 'business_profit_contribution',
                            'business_network_tax', 'property_tax',
                            'land_property_tax'])

def add_city_taxation(account):
    account.add_nodes({
        'home_tax': {
            'name': [u"Taxe d'habitation",
                     u"Taxe d'habitation (y compris THLV)",
                     u"Produits taxe d'habitation"],
            'type': 'section'
        },
        'compensation_2010': {
            'name': [u"Compensation-Relais 2010", u"Compensation-Relais"],
            'type': 'section'
        },
        'additionnal_land_property_tax': {
            'name': u"Taxe additionnelle à la taxe foncière sur les propriétés non bâties",
            'type': 'section'
        },
        'business_property_contribution': {
            'name': [u'Cotisation foncière des entreprises',
                     u'Cotisation foncière des entreprises (',
                     u"Cotisation foncière des entreprises au profit de l'Etat en 2010 ("],
            'type': 'section'
        },
        'retail_land_tax': {
            'name': u'Taxe sur les surfaces commerciales',
            'type': 'section'
        },
    })

    account.add_edges('taxation',
                      ['home_tax', 'property_tax', 'land_property_tax',
                       'additionnal_land_property_tax', 'compensation_2010',
                       'business_property_contribution', 'retail_land_tax'])

    add_tax_infos(account, ['home_tax', 'property_tax', 'land_property_tax', 'additionnal_land_property_tax', 'business_property_contribution', 'retail_land_tax', 'compensation_2010'])

def add_self_financing(account):
    account.add_nodes({
        'self_financing': {'name': u'AUTOFINANCEMENT', 'type': 'section'},
        'surplus': {'name': u'Excédent brut de fonctionnement'},
        'debt_repayment_capacity': {'name': u"CAF nette du remboursement en capital des emprunts"},
        'self_financing_capacity': {'name': [u"Capacité d'autofinancement = CAF",
                                             u"Capacité d'autofinancement brute=CAF"]},
    })
    account.add_edge('root', 'self_financing')
    account.add_edges('self_financing', ['self_financing_capacity', 'surplus',
                                         'debt_repayment_capacity'])

def make_base_account():
    # Base account for cities, epci, departments and regions
    account = Account()
    account.add_node('root', type='section')

    add_operating_operations(account)
    add_investments_operations(account)
    add_debt(account)
    add_taxation(account)

    return account

def make_region_account():
    account = make_base_account()

    account.add_nodes({
        'operating_real_revenues': {'name': u"produits de fonctionnement réels"},
        'direct_tax': {'name': u"Impôts directs"},
        'refund_tax': {'name': u"Fiscalité reversée"},
        'tipp': {'name': u"TIPP"},
        'training_and_learning_allocation': {'name': u"Dotation d'apprentissage et de formation professionnelle"},
        'realignment': {'name': [u"Attributions de péréquation et de compensation",
                                 u"attributions de péréquation et de compensation"]},
        'operating_real_costs': {'name': u"charges de fonctionnement réelles"},
        'subsidies_and_contingents': {'name': u'Subventions et contingents'},
        'mandatory_contributions_and_stakes': {'name': u'contributions obligatoires et participations'},
        'subsidies': {'name': 'subventions'},
        'individual_aids': {'name': u'aides à la personne'},
    })

    account.add_edges('operating_revenues',
                      ['operating_real_revenues', 'direct_tax', 'refund_tax',
                       'tipp', 'training_and_learning_allocation', 'realignment'])

    account.add_edges('operating_costs',
                      ['subsidies_and_contingents', 'mandatory_contributions_and_stakes',
                       'subsidies', 'individual_aids',
                       'operating_real_costs', ])

    # INVESTMENTS
    account.add_nodes({
        'sold_fixed_assets': {'name': u"Produits des cessions d'immobilisations"},
        'investments_direct_costs': {'name': u"Dépenses d'investissement directes"},
        'paid_subsidies': {'name': u"Subventions d'équipement versées"},
    })

    account.add_edges('investments', ['sold_fixed_assets', 'investments_direct_costs',
                                      'paid_subsidies'])

    return account

region_account = make_region_account()

def make_department_account():
    # TODO: edges are not well defined, review them.
    account = make_region_account()
    add_self_financing(account)

    account.add_nodes({
        'advertisement_tax': {'name': u"taxe départementale de publicité foncière et droits d'enregistrement"},
        'allocation_and_stake': {'name': u"Dotations et participations"},
        'pch': {'name': u'PCH'},
        'apa': {'name': u'APA'},
        'rsa': {'name': u'RSA'},
        'accomodation_costs': {'name': u"frais de séjour et d'hébergement"},
        'compensation_2010': {'name': u"Compensation-Relais 2010",
                              'type': 'section'},
        'home_tax': {
            'name': [u"Taxe d'habitation",
                     u"Taxe d'habitation (y compris THLV)",
                     u"Produits taxe d'habitation"],
            'type': 'section'
        },
    })
    account.add_edges('operating_revenues',
                      ['advertisement_tax', 'allocation_and_stake',])
    account.add_edges('operating_costs', ['pch', 'apa', 'rsa', 'accomodation_costs'])
    add_tax_infos(account, ['home_tax', 'compensation_2010'])

    return account

department_account = make_department_account()

def make_city_account():
    """Create city's account: note that there are little differences between fiscal
    years..."""

    account = make_base_account()
    add_self_financing(account)

    account.add_nodes({
        'localtax': {'name': u'Impôts Locaux'},
        'other_tax': {'name': u'Autres impôts et taxes'},
        'contingents': {'name': u'Contingents'}, # Find another name ?
        'paid_subsidies': {'name': u'Subventions versées'},
        'returned_properties': {'name': u"Retour de biens affectés, concédés, ..."},
        'facilities_expenses': {'name': u"Dépenses d'équipement"},
        'costs_to_allocate': {'name': u"Charges à répartir"},
        'fixed_assets': {'name': u"Immobilisations affectées, concédées, ..."},
        'advances_from_treasury': {'name': u'Avances du Trésor au 31/12/N'},
        'working_capital': {'name': u'FONDS DE ROULEMENT'},
    })
    account.add_edges('operating_revenues', ['localtax', 'other_tax'])
    account.add_edges('operating_costs', ['contingents', 'paid_subsidies'])
    account.add_edge('investments', 'returned_properties')
    account.add_edge('liabilities', 'advances_from_treasury')
    account.add_edges('investments_usage',
                      ['facilities_expenses', 'costs_to_allocate', 'fixed_assets'])
    account.add_edge('root', 'working_capital')

    add_city_taxation(account)

    return account

city_account = make_city_account()

def make_epci_account():
    account = make_base_account()
    add_city_taxation(account)
    add_self_financing(account)
    account.add_nodes({
        'tax_refund': {'name': u'Reversement de fiscalité'},
        'localtax': {'name': u'Impôts Locaux'},
        'other_tax': {'name': u'Autres impôts et taxes'},
        'paid_subsidies': {'name': u'Subventions versées'},
        'facilities_expenses': {'name': u"Dépenses d'équipement"},
    })
    account.add_edges('operating_revenues', ['tax_refund', 'localtax', 'other_tax'])
    account.add_edges('operating_costs', ['paid_subsidies'])
    return account

epci_account = make_epci_account()

