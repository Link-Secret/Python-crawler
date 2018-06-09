#@Time  :   2018/6/7 15:15
#@Author:   zjl
#@File  :   Today's_headline_Street_beat.py

import scrapy

class MeizituSpider(scrapy.Spider):
    name = 'meizitu'
    allowed_domains = ['meizitu.com']
    start_urls = ['https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D']

    def parse(self, response):
        pass