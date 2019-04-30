#@Time  :   2018/6/10 17:50
#@Author:   zjl
#@File  :   meizitu.py.py
import os
import requests
from requests import RequestException
from bs4 import BeautifulSoup
from hashlib import md5
from multiprocessing import Pool

# 访问索引页
def get_page_index(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 转换编码
            response.encoding = 'gb2312'
            #print(response.text)
            return response.text
        return None
    except RequestException:
        print('访问索引页出错',url)

# 处理索引页
def parse_page_index(html):
    soup = BeautifulSoup(html, 'lxml')
    page_urls = soup.select(".pic > a")
    for item in page_urls:
        print(item)
        yield item.attrs['href']


#访问详情页
def get_page_detail(url):
    print('正在访问',url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'gb2312'
            return response.text
        return None
    except RequestException:
        print('访问详情页出错',url)
        return None


# 解析详情页
def parse_page_detail(html):
    print('正在解析')
    soup = BeautifulSoup(html,'lxml')
    page_urls = soup.select('#picture > p > img')
    for page_url in page_urls:
        #print(page_url.attrs['src'])
        download_pic(page_url.attrs['src'])


#访问图片地址并下载
def download_pic(url):
    print('访问图片地址',url)
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    try:
        response = requests.get(url,headers = header)
        if response.status_code == 200:
            content = response.content
            file_path = '{0}/{1}.{2}'.format(os.getcwd()+'/picture2',md5(content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(content)
                    f.close()
                    print('ok')
    except RequestException:
        print('访问图片或存储出错')



def main(i):
    html = get_page_index('http://www.meizitu.com/a/more_'+ str(i) +'.html')
    # html.encode('utf-8')
    # parse_page_index使用yield生成器返回信息
    for detail_page_url in parse_page_index(html):
        detail_html = get_page_detail(detail_page_url)
        parse_page_detail(detail_html)
            #download_pic(pic_url)
    print('爬取完成')

if __name__ == '__main__':
    pool = Pool()
    # 多线程爬取第一页和第二页
    groups = [i for i in range(1,3)]
    pool.map(main,groups)



