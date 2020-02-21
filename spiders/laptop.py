# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import quote
from Jdlaptop.items import JdlaptopItem
from Jdlaptop.utils.common import get_mad5
import datetime
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider

class LaptopSpider(scrapy.Spider):
    name = 'laptop'
    #allowed_domains = ['https://search.jd.com/Search?keyword=']
    start_urls = ['https://search.jd.com/Search?keyword=']

    def start_requests(self):
        turl = self.start_urls[0]+quote(self.settings.get('KEYWORD'))
        for i in range(1,self.settings.get('MAX_PAGE')+1):
            yield scrapy.Request(url = turl,callback=self.parse,dont_filter=True,meta = {'page': i})

    def parse(self, response):

        goods = response.css('#J_goodsList .gl-item')
        for good in goods:
            item = JdlaptopItem()
            item['name'] = good.css('.p-name em::text').extract_first('')
            good_url = 'https:'+good.css('.p-commit a::attr(href)').extract_first('').replace('#comment','')
            item['good_url'] = good_url
            item['good_id'] = get_mad5(good_url)
            image= good.css('.p-img img::attr(data-lazy-img)').extract_first('')
            if image:
                item['image'] = ['http:'+image,]
            else:
                image = good.css('.p-img img::attr(src)').extract_first('')
                item['image'] = ['http:'+image,]
            item['price'] = good.css('.p-price em::text').extract_first()+good.css('.p-price i::text').extract_first()
            item['shop'] = good.css('.p-shop a::text').extract_first()
            item['crawl_time'] = datetime.datetime.now()
            yield item
