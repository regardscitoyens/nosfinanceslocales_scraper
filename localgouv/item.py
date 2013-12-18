from scrapy.item import Item, Field
from .account_network import (
    city_account,
    epci_account,
    department_account,
    region_account
)

# XXX: S...crapy stuff. I would prefer to return a dictionnary.

class FinancialData(Item):
    population = Field()
    zone_type = Field()
    name = Field()
    year = Field()
    url = Field()
    code = Field()

class CityFinancialData(FinancialData):
   insee_code = Field()
for line_name, line_attr in city_account.nodes.items():
    if 'type' not in line_attr:
        CityFinancialData.fields[line_name] = {}

class EPCIFinancialData(FinancialData):
    siren = Field()
for line_name, line_attr in epci_account.nodes.items():
    if 'type' not in line_attr:
        EPCIFinancialData.fields[line_name] = {}

class DepartmentFinancialData(FinancialData):
    insee_code = Field()
for line_name, line_attr in department_account.nodes.items():
    if 'type' not in line_attr:
        DepartmentFinancialData.fields[line_name] = {}

class RegionFinancialData(FinancialData):
    insee_code = Field()
for line_name, line_attr in region_account.nodes.items():
    if 'type' not in line_attr:
        RegionFinancialData.fields[line_name] = {}

