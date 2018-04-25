# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 对jobBole的item
class JobBoleArticleItem(scrapy.Item):
    # 指定字段，只有scrapy.filed()类型，所有类型都可以传递进来
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    # 对url进行MD5，将长度变成固定长度
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    # 本地地址
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()

    # 4.自动下载图片机制，修改setting，在item.pipelines中添加
    # E:\Envs\article_spider\Lib\site-packages\scrapy\pipelines\images.py