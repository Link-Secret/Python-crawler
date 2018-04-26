# -*- coding: utf-8 -*-

from scrapy.pipelines.images import ImagesPipeline
# 打开文件，codecs可以避免编码问题
import codecs
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 3.生效需要修改setting中的item.pipelines,将注释解开,并配置类名的优先级
# pipelines主要做数据存储
class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# 5.定制图片的一些功能,需要重载scrapy.pipelines.images.ImagesPipeline的一些函数
class ArticleImagePipeline(ImagesPipeline):
    # 这个item和jobbole中的article_item意义相当
    def item_completed(self, results, item, info):
        # results返回的第一个值是ok，第二个值是图片的路径
        for ok, value in results:
            image_file_path = value["path"]
        #得到image_file_path就将路径填充到items中
        item["image_file_path"] = image_file_path

        # 重写的pipeline需要return出去，因为下一个pipeline需要处理
        # （即setting中设置的，这个优先级为1，后面还有一个300(就是上面的ArticlespiderPipeline)）
        return item

# 6.下一步就是和数据库打交道，这里将数据保存到json文件里
class JsonWithEncodingPipeline(object):
    # 打开json文件
    def __init__(self):
        # 三个参数，文件名，以write方式打开（模式），文件编码
        self.file = codecs.open('article.json','w',encoding='utf-8')

    #处理item
    def process_item(self, item, spider):
        # 将item string类型转换成dictionary类型
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        # 和Java中的filter类似，filterChain.dofilter(),到下一个pipeline要处理
        return item

    #关闭文件
    def spider_closed(self,spider):
        self.file.close()