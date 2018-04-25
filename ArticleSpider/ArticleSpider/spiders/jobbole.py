# -*- coding: utf-8 -*-
import scrapy
import re
# 请求地址
from scrapy.http import Request
# 拼接URL地址的函数
from urllib import parse

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
        post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()
        # 对获取的当前页(所有文章页)的所有文章详情页地址遍历
        for post_url in post_urls:
            # 每个超链都调用parse_detail函数，得到具体的内容
            # yield Request(url = post_url,callback=self.parse_detail)

            '''伯乐网的超链是完整地址，只是为了演示有的网站超链基于当前地址（不是完整地址）所以使用这个URLjoin'''
            # yield关键字会自动交给scrapy进行下载
            # Request函数执行完url的爬取后都会调用(回调函数)self.parse_detail函数,即提取文章具体字段，循环即可
            yield Request(url= parse.urljoin(response.url,post_url),callback=self.parse_detail)

        '''2-提取下一页进行下载'''
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            # 此时回调函数继续执行是parse函数，即获取列表的所有文章地址，进行解析(整个流程是个递归，感觉）
            yield Request(url = parse.urljoin(response.url,next_url),callback=self.parse)

    '''提取文章的具体字段'''
    def parse_detail(self,response):
        # 得到标题
        # re_selector = response.xpath("/html/body/div[3]/div[3]/div[1]/div[1]/h1")
        # re2_selector = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()')
        # title1 = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract()[0]
        # create_date1 = response.xpath('//*[@id="post-110287"]/div[2]/p/text()').extract()[0].strip().replace("·","").strip()

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






        # ------------------------css选择----------------------
        '''css选择'''

        # ctitle = response.css(".entry-header h1::text").extract()
        # ccreate_date = response.css(".entry-meta-hide-on-mobile::text").extract()[0].strip().replace('·','').strip()
        # cparise_nums = response.css("")


        pass
