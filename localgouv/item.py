from scrapy.item import Item, Field

class FinancialData(Item):
    population = Field()
    zone_type = Field()
    name = Field()
    year = Field()
    url = Field()
    siren = Field()
    insee_code = Field()
    data = Field()
