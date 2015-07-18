from scrapy.item import Item, Field


class LocalFinance(Item):
    id = Field()
    data = Field()
