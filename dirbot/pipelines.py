from scrapy.exceptions import DropItem

class TiebaPipeline(object):
    def process_item(self, item, spider):
        return item
