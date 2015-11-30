import json
from scrapy.exceptions import DropItem


class FilterWordsPipeline(object):
    def __init__(self):
        self.file = open('items.json', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False).encode("utf-8").strip() + "\n"
        self.file.write(line)
        return item
