# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class JdlaptopItem(Item):
    # define the fields for your item here like:
    name = Field()
    good_url = Field()
    good_id = Field()
    image = Field()
    price = Field()
    shop = Field()
    crawl_time = Field()

    @property
    def get_insert(self):
        lis = tuple(dict(self).values())
        index = ','.join(['%s']*len(lis))
        dupli = ','.join([key+'=%s' for key in dict(self)])
        sql = "insert into laptop value({}) on duplicate key update {}".format(index,dupli)

        return sql,lis

    pass
