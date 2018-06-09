# -*- coding: utf-8 -*-
import scrapy

try:
    import urlparse as parse
except:
    from urllib import parse

class LagouSelSpider(scrapy.Spider):
    name = 'lagou_sel'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    headers = {
        "HOST": "www.lagou.com",
        "Referer": "https://www.lagou.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def parse(self, response):
        print("登录成功！")
        pass

    def start_requests(self):
        from selenium import webdriver
        browser = webdriver.Chrome(executable_path="E:/linuxShare/tools/chromedriver.exe")

        browser.get("https://passport.lagou.com/login/login.html?ts=1527215804172&serviceId=lagou&service=https%253A%252F%252Fwww.lagou.com%252F&action=login&signature=C483565396602FB12F095A46A9BD35CD")
        # 1.直接浏览器右键copy--selector-就可以选中
        browser.find_element_by_css_selector("body > section > div.left_area.fl > div:nth-child(2) > form > div:nth-child(1) > input").send_keys(
            "18202746477")
        browser.find_element_by_css_selector("body > section > div.left_area.fl > div:nth-child(2) > form > div:nth-child(2) > input").send_keys(
            "zxcvbnmu")
        browser.find_element_by_css_selector(
            "body > section > div.left_area.fl > div:nth-child(2) > form > div.input_item.btn_group.clearfix > input").click()
        # 2.自己分析，分析错了
        # browser.find_element_by_css_selector(".input_item,clearfix[0] input").send_keys(
        #     "18202746477")
        # browser.find_element_by_css_selector(".input_item,clearfix[1] input").send_keys(
        #     "zxcvbnmu")
        # browser.find_element_by_css_selector(
        #     ".input_item,btn_group,clearfix[0]").click()
        import time
        time.sleep(10)
        Cookies = browser.get_cookies()
        print(Cookies)
        cookie_dict = {}
        import pickle
        for cookie in Cookies:
            # 写入文件
            f = open('E:/linuxShare/scrapy/SpiderSelPra/cookies/lagou/' + cookie['name'] + '.lagou', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]
