# -*- coding: utf-8 -*-
import scrapy
import re
# 请求地址
from scrapy.http import Request
# 拼接URL地址的函数
from urllib import parse

# 存储字段,
# 8.4自定义itemloader，自定义规则
from ArticleSpider.items import JobBoleArticleItem,ArticleItemLoader

# utils工具类的common ，对url进行MD5，将长度变成固定长度
from ArticleSpider.utils.common import get_md5

# 转换日期成数据库中字date类型
import datetime

# itemloader,item管理容器
from scrapy.loader import ItemLoader

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
        # 实例化items.py中定义的item
        article_item = JobBoleArticleItem()

        # 得到标题
        # re_selector = response.xpath("/html/body/div[3]/div[3]/div[1]/div[1]/h1")
        # re2_selector = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()')
        # title1 = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract()[0]
        # create_date1 = response.xpath('//*[@id="post-110287"]/div[2]/p/text()').extract()[0].strip().replace("·","").strip()

        '''front_image_url字段  文章封面图'''
        front_image_url = response.meta.get("front_image_url", "")

        '''使用item_loader来开发'''
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace('·','').strip()
        # # 点赞数
        # praise_nums = int(response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0])
        #
        # # 收藏数
        # fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        # # 注意这里要非贪婪匹配
        # match_re = re.match(".*?(\d+).*",fav_nums);
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        #
        # # 评论数
        # comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        # match_re2 = re.match(".*?(\d+).*",comment_nums);
        # if match_re2:
        #     comment_nums = int(match_re2.group(1))
        # else:
        #     comment_nums = 0
        #
        # # 内容
        # content = response.xpath("//div[@class='entry']").extract()[0]
        #
        # # 标签 比如 职场 面试
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)
        #
        #
        # # 1.需要在items中字段设置
        # article_item["url_object_id"] = get_md5(response.url)
        #
        # article_item["title"] = title
        # # 将string类型的日期转换成date类型的日期
        # try:
        #     create_date = datetime.datetime.strptime(create_date,"%Y/%m/%d").date()
        # except Exception as e:
        #     # 如果转换异常则获取当前日期
        #     create_date = datetime.datetime.now().date()
        # article_item["create_date"] = create_date
        #
        # article_item["url"] = response.url
        # article_item["front_image_url"] = [front_image_url]  #图片地址是数组
        # article_item["praise_nums"] = praise_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["tags"] = tags
        # article_item["content"] = content



    #8. 通过item-loader加载item
        #item需要是实例
        #需要使用自定义规则的itemloader
        item_loader = ArticleItemLoader(item = JobBoleArticleItem(),response = response)
        # 添加规则
        item_loader.add_xpath("title",'//div[@class="entry-header"]/h1/text()')  #.add_css同样
        item_loader.add_value('url',response.url)
        item_loader.add_value('url_object_id',get_md5(response.url))
        item_loader.add_xpath('create_date',"//p[@class='entry-meta-hide-on-mobile']/text()")
        item_loader.add_value('front_image_url',[front_image_url])
        item_loader.add_xpath('praise_nums',"//span[contains(@class,'vote-post-up')]/h10/text()")
        item_loader.add_xpath('comment_nums', "//a[@href='#article-comment']/span/text()")
        item_loader.add_xpath('fav_nums', "//span[contains(@class,'bookmark-btn')]/text()")
        item_loader.add_xpath('tags', "//p[@class='entry-meta-hide-on-mobile']/a/text()")
        item_loader.add_xpath('content', "//div[@class='entry']")

        #规则解析,如果不配置规则，则返回的值都是list类型
        article_item = item_loader.load_item()


        # 2. 这个item会传递到pipelines中
        yield article_item




        # ------------------------css选择----------------------
        '''css选择'''

        # ctitle = response.css(".entry-header h1::text").extract()
        # ccreate_date = response.css(".entry-meta-hide-on-mobile::text").extract()[0].strip().replace('·','').strip()
        # cparise_nums = response.css("")

