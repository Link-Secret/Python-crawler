# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
# itemloader给item添加规则
from scrapy.loader.processors import MapCompose
# 转换日期成数据库中字date类型
import datetime


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 8.2   title添加的函数
def add_jobbole(value):
    return value + "-bobby"


#8.3 修改create_date为date类型
def date_convert(value):
    # 将string类型的日期转换成date类型的日期
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        # 如果转换异常则获取当前日期
        create_date = datetime.datetime.now().date()
    return create_date


# 对jobBole的item
class JobBoleArticleItem(scrapy.Item):
    # 指定字段，只有scrapy.filed()类型，所有类型都可以传递进来
    title = scrapy.Field(
        # 添加规则, MapCompose可以添加任意多函数
        # 这里必须名字为input_processor,
        input_processor = MapCompose(lambda x:x+"-jobbole",add_jobbole)
    )
    create_date = scrapy.Field(
        # 转换日期格式
        input_processor=MapCompose(date_convert)
    )
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