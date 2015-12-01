import json
from scrapy.exceptions import DropItem


class FilterWordsPipeline(object):
    def process_item(self, item, spider):
        return item
