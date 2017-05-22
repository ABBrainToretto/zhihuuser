# -*- coding: utf-8 -*-
import pymongo
from scrapy.conf import settings
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MongoPipeline(object):
    collection_name = 'users'

    def __init__(self):
        self.client = pymongo.MongoClient(host=settings.get('MONGO_URI')['MONGO_HOST'], port=settings.get('MONGO_URI')['MONGO_PORT'])
        self.db = self.client[settings.get('MONGO_DATABASE')['MONGO_DB']]  # 获得数据库的句柄
        # self.coll = self.db[settings['MONGO_COLL']]  # 获得collection的句柄

    def process_item(self,item,spider):
        self.db[self.collection_name].update({'url_token':item['url_token']},{'$set':dict(item)},True)
        return item
