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

class CityFinancialData(FinancialData):
   insee_code = Field()
for line_name, _ in city_account.iterlines():
    CityFinancialData.fields[line_name] = {}

class EPCIFinancialData(FinancialData):
    siren = Field()
for line_name, _ in epci_account.iterlines():
    EPCIFinancialData.fields[line_name] = {}

class DepartmentFinancialData(FinancialData):
    insee_code = Field()
for line_name, _ in department_account.iterlines():
    DepartmentFinancialData.fields[line_name] = {}

class RegionFinancialData(FinancialData):
    insee_code = Field()
for line_name, _ in region_account.iterlines():
    RegionFinancialData.fields[line_name] = {}

