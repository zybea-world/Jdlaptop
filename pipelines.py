# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import pymongo
from pymysql.cursors import DictCursor
from scrapy.exporters import JsonItemExporter
import logging


class TwismysqlPipeline(object):
    
    
    def __init__(self, dbpool):

        self.db = dbpool
        self.logger = logging.getLogger(__name__)

    @classmethod
    def from_crawler(cls, crawler):
        
        params = dict(
            host = crawler.settings.get('HOST'),
            user = crawler.settings.get('USER'),
            password = crawler.settings.get('PASSWD'),
            db = crawler.settings.get('DB'),
            cursorclass = DictCursor,
            charset = 'utf8',
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool('pymysql',**params)
        return cls(dbpool)

    def process_item(self, item, spider):
        
        if spider.name == 'laptop':
            query = self.db.runInteraction(self.do_insert, item)
            self.logger.error(query)
            #query.addCallback(self.handle_error)
            return item

   #def handle_error(self, failure):
   #    print(failure)

    def do_insert(self, cursor, item):
        
        sql,values = item.get_insert
        cursor.execute(sql, values*2)

    def close_spider(self,spider):
        
        self.db.close()


class JsonPipeline(object):

    def __init__(self):

        self.f = open('laptop.json','wb')
        self.exporter = JsonItemExporter(self.f, indent=2, ensure_ascii=False,)

    def open_spider(self,spider):

        self.exporter.start_exporting()

    def process_item(self, item, spider):

        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        
        self.exporter.finish_exporting()
        self.f.close()
        pass

class MongodbPipeline(object):

    @classmethod
    def from_crawler(cls,crawler):
        parmas = dict(
            host = crawler.settings.get('HOST'),
            port = crawler.settings.get('PORT'),
        )
        db = crawler.settings.get('DB')
        col = crawler.settings.get('COL')
        client = pymongo.MongoClient(**parmas)
        return cls(client,col,db)

    def __init__(self, client, col, db):

        self.client = client
        self.db = self.client[db]
        self.col = self.db[col]
        self.logger = logging.getLogger(__name__)

    def process_item(self,item,spider):

        if spider.name == 'laptop':
            result = self.col.insert(dict(item))
            self.logger.error(result)
        return item

    def close_spider(self,spider):

        self.client.close()




class JdlaptopPipeline(object):
    def process_item(self, item, spider):
        return item
