#@Time  :   2018/5/2 10:11
#@Author:   zjl
#@File  :   selenium_spider.py

from selenium import webdriver
# 获取数据
from scrapy.selector import Selector

# 获取driver
browser = webdriver.Chrome(executable_path="E:/linuxShare/tools/chromedriver.exe")
# 访问对应的页面
# browser.get("http://www.cnblogs.com/alex3714/p/7966656.html#3960892")

browser.get("https://www.zhihu.com/signin?next=http%3A%2F%2Fwww.zhihu.com%2F")

# 向input框输入内容
browser.find_element_by_css_selector(".SignFlow-account input[name='username']").send_keys('1078184113@qq.com')
browser.find_element_by_css_selector(".SignFlow-password input[name='password']").send_keys("zxcvbnmu")

# 登录
browser.find_element_by_css_selector(".Login-options button.SignFlow-submitButton").click()

# 模拟人访问获得网页加载JS后的代码，注意，这里是加载js后的
# 源代码，而不是网页源代码
print(browser.page_source)

# 获取数据
# t_selector = Selector(text=browser.page_source)
# print(t_selector.css("title").extract()[0])




browser.quit()