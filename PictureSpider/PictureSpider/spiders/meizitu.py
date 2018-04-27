# -*- coding: utf-8 -*-
import scrapy


class MeizituSpider(scrapy.Spider):
    name = 'meizitu'
    allowed_domains = ['meizitu.com']
    start_urls = ['http://meizitu.com/']

    def parse(self, response):
        pass
