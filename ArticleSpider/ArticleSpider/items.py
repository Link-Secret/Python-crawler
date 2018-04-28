# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
# 1,itemloader给item添加输入规则 ,2,输出规则-只输出第一个，3，输出规则-输出格式join连接
from scrapy.loader.processors import MapCompose,TakeFirst,Join
# 转换日期成数据库中字date类型
import datetime
# 正则
import re


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


#8.5得到数字（将后面的评论，点赞等字符删除
def get_nums(value):
    match_re = re.match(".*?(\d+).*", value);
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


#8.6 将标签中的评论删除
def remove_comment_tags(value):
    #将标签value(list)中的'n评论'删除
    if '评论' in value:
        return ''
    else:
        return value


#8.7 将front_image_url的value返回，因为如果不继承默认itemloadr就是返回list，
# 这里将默认itemloader的返回(default_output_processor = TakeFirst())覆盖即可
def return_value(value):
    return value

# 8.4 默认规则类,自定义itemloader
class ArticleItemLoader(ItemLoader):
    # jobbole.py中使用当前itemloader类实例，默认输出第一个TakeFirst
    # (因为scrapy的itemloader输出的是list,所以使用自定义listloader)
    default_output_processor = TakeFirst()

# 对jobBole的item
class JobBoleArticleItem(scrapy.Item):
    # 指定字段，只有scrapy.filed()类型，所有类型都可以传递进来
    title = scrapy.Field(
        # 添加规则, MapCompose可以添加任意多函数
        # 这里必须名字为input_processor,
        # input_processor = MapCompose(lambda x:x+"-jobbole",add_jobbole)
    )
    create_date = scrapy.Field(
         # 转换日期格式
        input_processor=MapCompose(date_convert),
        #out_processor = TakeFirst  #注释是因为现在默认输出第一个
    )
    url = scrapy.Field()
    # 对url进行MD5，将长度变成固定长度
    url_object_id = scrapy.Field()
    # front_image_url  #图片地址是数组,所以要配相应的规则,将list转换成数组
    front_image_url = scrapy.Field(
        output_processor = MapCompose(return_value)
        #还有一个SQL语句中需要修改为只获取list的第一个值
    )
    # 本地地址
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor = MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        # 修改输入规则
        input_processor = MapCompose(remove_comment_tags),
        #修改默认只输出第一个的规则,改为连接输出
        output_processor = Join(',')
    )
    content = scrapy.Field()

    # 4.自动下载图片机制，修改setting，在item.pipelines中添加
    # E:\Envs\article_spider\Lib\site-packages\scrapy\pipelines\images.py