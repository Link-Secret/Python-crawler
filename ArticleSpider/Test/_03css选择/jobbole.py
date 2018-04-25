# -*- coding: utf-8 -*-
import scrapy
import re


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/110287']

    def parse(self, response):
        # 得到标题，注释第一个为错误的。scrapy选择的是网页没有执行JavaScript的源码
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

        ctitle = response.css(".entry-header h1::text").extract()
        ccreate_date = response.css(".entry-meta-hide-on-mobile::text").extract()[0].strip().replace('·', '').strip()
        # cparise_nums = response.css("")



        pass
