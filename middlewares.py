# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
from scrapy.xlib.pydispatch import dispatcher
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
import time


class SeleMiddleware(object):


    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        dispatcher.connect(s.spider_opened, signals.spider_opened)
        return s

    def __init__(self):

        op = webdriver.ChromeOptions()
        op.add_experimental_option('debuggerAddress','127.0.0.1:9222')#远程调试模式，防止识别为非人工操作
        #op.add_argument("--headless")#无头模式
        op.add_argument('--disable-extensions')#禁止加载拓展
        #prefs = { 'profile.default_content_setting_values': { 'images': 2 } }
        #op.add_experimental_option("prefs",prefs)#禁止加载图片
        self.br = webdriver.Chrome(options=op)
        self.wait = WebDriverWait(self.br,15)#设置最长等待时间

    def process_request(self,request,spider):

        if '360buyimg.com' not in request.url:#防止image链接进入,会导致图片无法获取，且报错
            page = request.meta.get('page')
            self.br.get(request.url)
            if page > 1:
                skip = self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="J_bottomPage"]/span[2]/input')))
                skip.send_keys(Keys.CONTROL,'a')
                #skip.clear()
                skip.send_keys(page)
                skip.send_keys(Keys.ENTER)
            self.br.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(3)
            return HtmlResponse(url = self.br.current_url,body=self.br.page_source,status=200,encoding='utf-8',request=request)

    def spider_closed(self, spider):
        pass
        #self.br.close()

    def spider_opened(self, spider):
        pass


class UseragentMiddleware(object):


    def process_request(self, request, spider):
        ua = UserAgent()
        user_agent = ua.chrome
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)


class JdlaptopSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JdlaptopDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
