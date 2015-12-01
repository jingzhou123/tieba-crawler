from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    description = Field()
    url = Field()

class Tieba(Item):
    name = Field()
    owners = Field()
