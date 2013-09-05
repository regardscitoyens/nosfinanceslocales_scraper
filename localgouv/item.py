from scrapy.item import Item, Field
from .account_network import make_city_account

class CityFinancialData(Item):
    population = Field()
    zone_type = Field()
    name = Field()
    insee_code = Field()
    year = Field()

city_account = make_city_account()

for line_name, _ in city_account.iterlines():
    CityFinancialData.fields[line_name] = {}



