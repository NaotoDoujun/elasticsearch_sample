# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json, types, hashlib
from six import string_types
from itemadapter import ItemAdapter
from elasticsearch import Elasticsearch, helpers

class SampleCrawlerPipeline:
    es = None
    items_buffer = []

    def __init__(self, settings):
        self.settings = settings
        self.es = Elasticsearch(self.settings['ELASTICSEARCH_SERVER'],timeout=100)
        super(SampleCrawlerPipeline, self).__init__

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def process_unique_key(self, unique_key):
        if isinstance(unique_key, (list, tuple)):
            unique_key = unique_key[0].encode('utf-8')
        elif isinstance(unique_key, string_types):
            unique_key = unique_key.encode('utf-8')
        else:
            raise Exception('unique key must be str or unicode')

        return unique_key

    def get_id(self, item):
        item_unique_key = item[self.settings['ELASTICSEARCH_UNIQ_KEY']]
        if isinstance(item_unique_key, list):
            item_unique_key = '-'.join(item_unique_key)

        unique_key = self.process_unique_key(item_unique_key)
        item_id = hashlib.sha1(unique_key).hexdigest()
        return item_id

    def create_index(self):
        if self.settings['ELASTICSEARCH_INDEX_RECREATE']:
            if self.es.indices.exists(index=self.settings['ELASTICSEARCH_INDEX']):
                self.es.indices.delete(index=self.settings['ELASTICSEARCH_INDEX'])
        
        with open(self.settings['ELASTICSEARCH_MAPPING_PATH']) as f:
            mapping = json.load(f)
            self.es.indices.create(index=self.settings['ELASTICSEARCH_INDEX'], body=mapping)

    def index_item(self, item):
        if not self.es.indices.exists(index=self.settings['ELASTICSEARCH_INDEX']):
            self.create_index()

        index_action = {
            '_index': self.settings['ELASTICSEARCH_INDEX'],
            '_source': dict(item)
        }
        if self.settings['ELASTICSEARCH_UNIQ_KEY'] is not None:
            item_id = self.get_id(item)
            index_action['_id'] = item_id
        self.items_buffer.append(index_action)
        if len(self.items_buffer) >= self.settings.get('ELASTICSEARCH_BUFFER_LENGTH', 500):
            self.send_items()
            self.items_buffer = []

    def send_items(self):
        helpers.bulk(self.es, self.items_buffer)

    def process_item(self, item, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):
            for each in item:
                self.process_item(each, spider)
        else:
            self.index_item(item)
            return item

    def close_spider(self, spider):
        if len(self.items_buffer):
            self.send_items()
