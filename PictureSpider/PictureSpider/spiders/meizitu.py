# -*- coding: utf-8 -*-
import scrapy
# request
from scrapy.http import Request
# 拼接URL地址的函数
from urllib import parse
# 正则
import re
# 字段引进
from PictureSpider.items import meizituItem

class MeizituSpider(scrapy.Spider):
    name = 'meizitu'
    allowed_domains = ['meizitu.com']
    start_urls = ['http://meizitu.com/a/more_1.html']

    def parse(self, response):
        # 解析列表中的所有详细页的地址url
        img_urls = response.css('.wp-item .pic a::attr(href)').extract()

        # 遍历
        for img_url in img_urls:
            yield Request(url=parse.urljoin(response.url,img_url),callback=self.parse_detail)

        #下一页继续遍历
        next_url = response.css('#wp_page_numbers li a::attr(href)').extract()[-2]
        next_text = response.css('#wp_page_numbers li a::text').extract()[-2]
        if next_text == "下一页":
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)

    # 提取详情页图片
    def parse_detail(self,response):
        meizitu_item = meizituItem()

        front_image_url = response.css('#picture img::attr(src)').extract()

        meizitu_item['front_image_url'] = front_image_url

        yield meizitu_item