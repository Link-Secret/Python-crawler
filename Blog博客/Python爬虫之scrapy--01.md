>github:https://github.com/Link-Secret/Python-crawler
1. 准备工作

    1. 虚拟环境
    >mkvirtualenv article_spider
    
    2. 安装scrapy
    >pip install scrapy(可以选择豆瓣源，豆瓣源速度比较快)
    
    >如果安装Twisted出错，下载Twisted对应的whl文件安装即可
    
    3. 创建一个基于scrapy模板的新project(项目) 
    >cd 项目地址
    
    >进入scrapy虚拟环境
    
    >scrapy startproject 项目名
    
    4. 使用pycharm打开项目，并将当前项目虚拟环境指向准备的虚拟环境
    
2. 开始
    
    1. 创建爬虫文件
    > cd 项目名  进入项目目录

    > scrapy genspider jobole(爬虫文件名) blog.jobbole.com(爬虫爬取网站)
    
    > 源码解析：
 
    ``` 
        jobbole.py文件
 
    
    class JobboleSpider(scrapy.Spider):
        name = 'jobbole'
        allowed_domains = ['blog.jobbole.com']
        start_urls = ['http://blog.jobbole.com/']

        Scrapy源码文件init.py
    scrapy.Spider中有个start_requests函数 
     def start_requests(self):会遍历start_urls然后将值传给
     def make_requests_from_url(self, url):会将request交给scrapy下载器
     下载完成后会返回(response)到jobbole.py文件下的
      def parse(self, response):
        pass
    ```
    
    2. 如何调试，pycharm没有scrapy格式的项目，所以要新建一个main.py文件(建立在项目名(最顶层)目录下)来调试
    ```
    from scrapy.cmdline import execute

    import sys
    import os

    os.path.abspath(__file__)#获取当前main文件的路径
    os.path.dirname(file)#得到file文件的父目录路径
    print(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    #scrapy启动jobbole.py 命令为 scrapy crawl 文件名，所以使用数组保存这三个字符
    execute(["scrapy","crawl","jobbole"])
    ```
    > win下运行会出错 No module named 'win32api'
    
    >pip install pypiwin32
    
    >scrapy：scrapy启动一个spider的命令为 
    
    >scrapy crawl jobbole(spider名)
    
    3. robots协议,默认遵守，修改为FALSE
    
    
3. 爬取jobbole文章

    前置，我们可以在cmd下先将整个网页下载下来，在用选择器调试是否选择上对应元素，
    例子：
    >(article_spider) E:\linuxShare\ArticleSpider>scrapy shell http://blog.jobbole.com/110287/

    > title = response.xpath('//div[@class="entry-header"]/h1/text()')
    
    >title.extract()[0]
    
    >'2016 腾讯软件开发面试题（部分）'

    1.xpath选择器
    
        ```
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace('·','').strip()
        # 点赞数
        praise_nums = int(response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0])

        # 收藏数
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        # 注意这里要非贪婪匹配
        match_re = re.match(".*?(\d+).*",fav_nums);
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        # 评论数
        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_re2 = re.match(".*?(\d+).*",comment_nums);
        if match_re2:
            comment_nums = int(match_re2.group(1))
        else:
            comment_nums = 0

        # 内容
        content = response.xpath("//div[@class='entry']").extract()[0]

        # 标签 比如 职场 面试
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
        ```
        
    2. css选择器(推荐)
        ```
        title = response.css('.entry-header h1::text').extract()[0]
        
        create_date = response.css('p.entry-meta-hide-on-mobile::text').extract().strip().replace('·','').strip()
        
        praise_nums = response.css('.vote-post-up h10::text').extract()[0]
        
        content = respnse.css('.entry').extract()
        
        tag_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()

        
        ```
    3. 爬取伯乐网所有文章
        > 分析：
        
        >http://blog.jobbole.com/all-posts/
        
        这个地址可以获得所有文章的地址，我们就以这个网址来作为起始地址
        
        从第一页到最后一页，遍历每一页的文章，每一篇文章都调用parse_detail方法得到具体的title和create_date等信息
        
        流程：
        1. 启动class JobboleSpider(scrapy.Spider):类
        2. Spider会调用__init__.py(scrapy类)的start_requests方法，接着会调用make_requests_from_url，这个方法会返回scrapy下载器下载的内容response
        3. 接着返回爬虫.py文件中的parse方法，此时response中就有下载器下载的内容，我们就可以使用xpath(css)选择器来选出内容
        4. 首先我们将当前页的所有文章详情页的地址选择出来，遍历文章详情页(调用parse_detail方法)
        5. 当遍历完成第一页的所有文章详情页的内容后，接着提取下一页的超链地址(使用Request方法请求,返回值再)调用(parse)自身从而得到第二页的列表页得到第二页的所有文章详情页，直到没有下一页
        
        
        
        
        
        
        
        ```
        class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        '''获取伯乐网所有文章
                1. 获取文章列表页中的文章URL并交给scrapy下载后并进行解析
                2. 获取下一页URL并交给scrapy下载，下载完成后交给parse
        '''

        '''1-解析列表页中的所有文章URL并交给scrapy下载后并进行解析'''
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        # 对获取的当前页(所有文章页)的所有文章详情页地址遍历
        for post_node in post_nodes:
            # 使用post_node节点的img选择器
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")


            # 每个超链都调用parse_detail函数，得到具体的内容
            # yield Request(url = post_url,callback=self.parse_detail)

            '''伯乐网的超链是完整地址，只是为了演示有的网站超链基于当前地址（不是完整地址）所以使用这个URLjoin'''
            # yield关键字会自动交给scrapy进行下载
            # Request函数执行完url的爬取后都会调用(回调函数)self.parse_detail函数,即提取文章具体字段，循环即可
            yield Request(url= parse.urljoin(response.url,post_url), meta={"front_image_url":image_url}, callback=self.parse_detail)

        '''2-提取下一页进行下载'''
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            # 此时回调函数继续执行是parse函数，即获取列表的所有文章地址，进行解析(整个流程是个递归，感觉）
            yield Request(url = parse.urljoin(response.url,next_url),callback=self.parse)

    '''提取文章的具体字段'''
    def parse_detail(self,response):
        # 图片
        article_item = JobBoleArticleItem()

        # 得到标题
        # re_selector = response.xpath("/html/body/div[3]/div[3]/div[1]/div[1]/h1")
        # re2_selector = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()')
        # title1 = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract()[0]
        # create_date1 = response.xpath('//*[@id="post-110287"]/div[2]/p/text()').extract()[0].strip().replace("·","").strip()

        '''front_image_url字段  文章封面图'''
        front_image_url = response.meta.get("front_image_url", "")

        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace('·','').strip()
        # 点赞数
        praise_nums = int(response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0])

        # 收藏数
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        # 注意这里要非贪婪匹配
        match_re = re.match(".*?(\d+).*",fav_nums);
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        # 评论数
        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_re2 = re.match(".*?(\d+).*",comment_nums);
        if match_re2:
            comment_nums = int(match_re2.group(1))
        else:
            comment_nums = 0

        # 内容
        content = response.xpath("//div[@class='entry']").extract()[0]

        # 标签 比如 职场 面试
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

    
        ```
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        