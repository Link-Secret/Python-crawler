# -*- coding: utf-8 -*-
import scrapy
import re
#
from scrapy.http import Request
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

        '''解析列表页中的所有文章URL并交给scrapy下载后并进行解析'''
        post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()
        for post_url in post_urls:
            # 每个超链都调用parse_detail函数，得到具体的内容
            yield Request(url= parse.urljoin(response.url,post_url),callback=self.parse_detail())
            print(post_url)



    def parse_detail(self,response):
        # 得到标题
        # re_selector = response.xpath("/html/body/div[3]/div[3]/div[1]/div[1]/h1")
        # re2_selector = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()')
        title1 = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract()[0]
        create_date1 = response.xpath('//*[@id="post-110287"]/div[2]/p/text()').extract()[0].strip().replace("·","").strip()

        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace('·','').strip()
        # 点赞数
        praise_nums = int(response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0])

        # 收藏数
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        # 注意这里要非贪婪匹配
        match_re = re.match(".*?(\d+).*",fav_nums);
        if match_re:
            fav_nums = match_re.group(1)

        # 评论数
        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_re2 = re.match(".*?(\d+).*",comment_nums);
        if match_re2:
            comment_nums = match_re2.group(1)

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
