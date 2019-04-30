#@Time  :   2018/6/9 10:30
#@Author:   zjl
#@File  :   maoyanTop100.py
import json

import requests
from requests.exceptions import RequestException #异常
import re #正则
from multiprocessing import Pool

# 获取页面
def get_one_page(url):
    # 反爬虫，设置用户请求头
    header = {
        'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
    }
    # 得到网页地址的内容
    try:
        response = requests.get(url,headers = header)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


# 解析页面
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>'
                         '.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">'
                         '(.*?)</i>.*?</dd>',re.S)

    itmes = re.findall(pattern,html);
    for itme in itmes:
        yield {
            'index': itme[0],
            'image': itme[1],
            'title': itme[2],
            'actor': itme[3].strip()[3:],
            'time': itme[4].strip()[5:],
            'score': itme[5]+itme[6]
        }
    # print(itmes)


# 存储数据
def write_to_file(content):
    # a参数代表往后追加
    with open('result.txt','a', encoding= 'utf-8') as f:
        # 一个content代表一个item，后面要换行
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

# offset设置爬取下一页
def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        write_to_file(item)
        print(item)

# 单线程
# if __name__ == "__main__":
#     for i in range(10):
#         main(i*10)

# 多线程爬取
if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])
