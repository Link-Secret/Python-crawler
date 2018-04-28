# -*- coding: utf-8 -*-

from scrapy.pipelines.images import ImagesPipeline
# 打开文件，codecs可以避免编码问题
import codecs
import json
# scrapy json格式文件导入包
from scrapy.exporters import JsonItemExporter
# mysql，导入数据到数据库
import MySQLdb
# 异步导入数据库，使用Twisted模块
from twisted.enterprise import adbapi
import MySQLdb.cursors

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
        item["front_image_path"] = image_file_path

        # 重写的pipeline需要return出去，因为下一个pipeline需要处理
        # （即setting中设置的，这个优先级为1，后面还有一个300(就是上面的ArticlespiderPipeline)）
        return item

# 6.下一步就是和数据库打交道，这里将数据保存到json文件里
'''6.1自定义类导出json文件'''
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


'''6.2 利用scrapy提供的json exporter导出json格式文件'''
class jsonExporterPipleline(object):
    def __init__(self):
        # wb,二进制
        self.file = open("articleexport.json",'wb')
        self.exporter = JsonItemExporter(self.file, encoding = "utf-8",ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        # 停止导出
        self.exporter.finish_exporting()
        # 文件关闭
        self.file.close()

    # 处理item
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


'''7，7.1 方法一：将数据导入到数据库中（同步） '''
class MysqlPipeline(object):
    def __init__(self):
        # 连接数据库
        #self.conn = MySQLdb.connect('host','user','password','dbname',charset='utf8',use_unicode = True)
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'admin', 'article_spider', charset='utf8', use_unicode=True)
        # 获取cursor
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        insert_sql = """
            insert into jobbole_article(title,url,create_date,fav_nums, url_object_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql,(item['title'],item['url'],item['create_date'],item['fav_nums'],item['url_object_id']))
        self.conn.commit()


''''7，7.2 方法二：将数据导入到数据库中（异步）Twisted提供 '''
class MysqlTwistedPipeline(object):
        # 接收cls(classmethod中)实例化的参数
        def __init__(self, dbpool):
            self.dbpool = dbpool

        #setting中设置Host，user，password
        # 从setting中得到配置参数
        # 相当于构造函数
        @classmethod
        def from_settings(cls,settings):    #from_settings 写错成setting会无法正常调用，和类名要相同
            # dict类型的可变参数
            dbparms = dict(
                host = settings['MYSQL_HOST'],
                db = settings['MYSQL_DBNAME'],
                user = settings['MYSQL_USER'],
                passwd = settings['MYSQL_PASSWORD'],
                charset = 'utf8',
                cursorclass = MySQLdb.cursors.DictCursor,
                use_unicode = True,
            )
            dbpool = adbapi.ConnectionPool("MySQLdb",**dbparms)
            # 跳转到init中，
            return cls(dbpool)

        def process_item(self,item,spider):
            # 异步执行
            query = self.dbpool.runInteraction(self.do_insert,item)
            #错误(异常)处理
            query.addErrback(self.handle_error)

        #错误处理函数
        def handle_error(self,failure):
            #处理异步插入的异常
            print(failure)

        def do_insert(self,cursor,item):
            # 执行具体的插入
            insert_sql = """
                        insert into jobbole_article(title,url,create_date,fav_nums, url_object_id)
                        VALUES (%s, %s, %s, %s, %s)
                    """
            cursor.execute(insert_sql, (
            item['title'], item['url'], item['create_date'], item['fav_nums'], item['url_object_id']))
