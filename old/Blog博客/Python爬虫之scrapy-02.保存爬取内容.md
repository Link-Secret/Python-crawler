1. item

    1. 在jobbole.py中得到数据的时候，配置完item后，如果scrapy发现保存的是item类的实例(即数据保存的字段相匹配)的时候，就会直接将这个item路由到pipeline中，这样就可以在pipeline中集中处理数据
    
    2. Request的另一个变量meta，传递的是字典，传递图片的URL(这个URL没有域名，所以使用urljoin方法，组合地址)
    
    3. 将items.py中配置的类导入到jobbole.py中，实例化item的实例，然后将jobbole.py中的字段填充到item实例的配置的字段
    ```
    items.py
    
    对jobBole的item
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
    
    ```
    
    ```
    jobbole.py
    
    # 存储字段
    from ArticleSpider.items import JobBoleArticleItem
    
    # 实例化items.py中定义的item
    article_item = JobBoleArticleItem()
    
    article_item["create_date"] = create_date
    article_item["url"] = response.url
    article_item["front_image_url"] = [front_image_url]  #图片地址是数组
    article_item["praise_nums"] = praise_nums
    article_item["comment_nums"] = comment_nums
    article_item["fav_nums"] = fav_nums
    article_item["tags"] = tags
    article_item["content"] = content
    
    # 2.这个item会传递到pipelines中
    yield article_item
    
    ```    
    4. 图片下载
       1. scrapy相应的pipeline(ImagePipeline)有下载功能
         在setting中的
            >ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1,}
            
            > IMAGES_URLS_FIELD = "front_image_url" #配置字段(注意格式为数组,所以front_image_url对应的格式要为数组)
            
            ```
            #设置图片保存路径
            #file代表当前文件，os.path.dirname(__file__)就代表file的dir（即文件夹）
            project_dir = os.path.abspath(os.path.dirname(__file__))
            IMAGES_STORE = os.path.join(project_dir,"images")
            ```
            >安装保存图片的库 pip install pillow
            
        2.自己定制(继承scrapy包ImagePipeline的pipeline)
        
        >重写需要定制功能的方法
        
        >重写item_completed方法，图片保存地址的字段的功能
        
        ```
        # 5.定制图片的一些功能,需要重载scrapy.pipelines.images.ImagesPipeline的一些函数
        class ArticleImagePipeline(ImagesPipeline):
        # 这个item和jobbole中的article_item意义相当
        def item_completed(self, results, item, info):
        # results返回的第一个值是ok，第二个值是图片的路径
        for ok, value in results:
            image_file_path = value["path"]
        #得到image_file_path就将路径填充到items中
        item["front_image_path"] = image_file_path
        ```
        
    5. items中的url_object_id字段
        > url_object_id = scrapy.Field()  #对url进行MD5，将长度变成固定长度
        
        ```
        common.py
        # 7.对url进行MD5，将长度变成固定长度
            def get_md5(url):
            # 判断传入的URL是否是Unicode
                if isinstance(url,str):
                url = url.encode("UTF-8")
                m = hashlib.md5()
                m.update(url)
                # 抽取摘要
                return m.hexdigest()
        ```
    
2. pipeline
    1. pipelines.py
    pipelines中可以配置多个pipeline类，每个pipeline都可以接收传递来的item(前提是在setting中配置了，配置中按数值大小决定优先级)
        > settings.py
        
        >ITEM_PIPELINES = {...数值越小优先级越高...}

    2. 
    

3. 保存到json文件中
    1. 在pipelines.py中定义一个保存为json文件的pipeline类
    

    ```
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
    
    # scrapy json格式文件导入包,import可以选择不同格式
    from scrapy.exporters import JsonItemExporter
    
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

    ```
    
4. 依据item中字段创建数据库
    1. 其中创建时间字段需要从字符串转换成Date类型
    2. >pip install mysqlclient

    