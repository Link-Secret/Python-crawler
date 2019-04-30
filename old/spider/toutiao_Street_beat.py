#@Time  :   2018/6/10 8:58
#@Author:   zjl
#@File  :   toutiao_Street_beat.py
import json
from json.decoder import JSONDecodeError
from urllib.parse import urlencode
from hashlib import md5

import os
import pymongo
import requests
from requests import RequestException
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool

#
MONGO_URL = 'localhost'
MOGO_DB = 'toutiao'
MOGO_TABLE = 'toutiao'

# 循环
GROUP_START = 1
GROUP_END = 20


client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MOGO_DB]



def get_page_index(offset,keyword):
    # 分析请求头，当页面滑动至页面底部的时候，会发送Ajax请求
    # Request URL: https://www.toutiao.com/search_content/?
    # offset=40&
    # format=json&
    # keyword=%E8%A1%97%E6%8B%8D&
    # autoload=true&
    # count=20&
    # cur_tab=1&
    # from=search_tab
    header = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    data = {
        "offset": offset,
        "format": "json",
        "keyword": keyword,
        "autoload": "true",
        "count": 20,
        "cur_tab": 1,
        "from": "search_tab"
    }
    url = "https://www.toutiao.com/search_content/?" + urlencode(data)
    print(url)

    try:
        response = requests.get(url,headers = header)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        print("访问索引页出错")
        return None


#对索引页的链接地址进行分析
def parse_page_index(html):
    try:
        data = json.loads(
            html)  # supporting text file or binary file containing a JSON document) to a Python object using this conversion table.
        if data and 'data' in data.keys():
            for item in data.get('data'):
                # 由于返回的json数据中有干扰项，需要清除干扰项
                if item.get('article_url'):
                    yield item.get('article_url')
                else:
                    pass
    except JSONDecodeError:
        pass


# 访问详情页
def get_page_detail(url):
    # 这里头条有反爬虫措施，如果没有设置请求头会301
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    try:
        response = requests.get(url,headers = header)
        if response.status_code == 200:
            #print(response.text)
            return response.text
        return None
    except RequestException:
        print("访问详情页出错",url)
        return None


# 解析详情页
def parse_page_detail(html, url):
    # 使用BeautifulSoup解析,安装lxml解析器
    soup = BeautifulSoup(html,'lxml');
    title = soup.select('title')[0].get_text()
    #print(title)
    images_pattern = re.compile('gallery: JSON.parse\("(.*?)"\)', re.S)
    #images_pattern = re.compile('pgc-image/(.*?)",')
    result = re.search(images_pattern, html)
    #print(result)
    #print(result.group(1))
    # 对正则匹配的字符进行处理
    try:
        resultRe = result.group(1).replace('\\','')
    except Exception:
        pass
    if result:
        #print(result.group(1))
        data = json.loads(resultRe)
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            #print(images)
            for image in images:dowonload_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }


# 存储进MongoDB数据库
def save_to_mongo(result):
    if db[MOGO_TABLE].insert(result):
        print('存储到MongoDB成功',result)
        return True
    return False

# 下载图片
def dowonload_image(url):
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    print('正在下载',url)
    try:
        response = requests.get(url,headers = header)
        if response.status_code == 200:
            # 存储图片
            save_image(response.content)
        else:
            return None
    except RequestException:
        print('请求图片页出错',url)
        return None


# 存储图片
def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd()+'/picture',md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()


def main(offset):
    html = get_page_index(offset, '街拍')
    # print(html)
    for url in parse_page_index(html):
        #print(url)
        # 'http://toutiao.com/group/6565057165717930504/' --->  'https://www.toutiao.com/a6565057165717930504/'
        # print(url)
        # url = url[0:19] + 'a' + url[25:]
        html = get_page_detail(url)
        #print(html)
        if html:
            result = parse_page_detail(html, url)
            #print(result)
            if result: save_to_mongo(result)


if __name__ == '__main__':
    #main()
    groups = [x*20 for x in range(GROUP_START,GROUP_END+1)]
    pool = Pool()
    pool.map(main, groups)
