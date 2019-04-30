#@Time  :   2018/4/25 20:47
#@Author:   zjl
#@File  :   common.py
import hashlib

# 7.对url进行MD5，将长度变成固定长度
def get_md5(url):
    # 判断传入的URL是否是Unicode
    if isinstance(url,str):
        url = url.encode("UTF-8")
    m = hashlib.md5()
    m.update(url)
    # 抽取摘要
    return m.hexdigest()

if __name__ == "__main__":
    print(get_md5("http://jobbole.com".encode("UTF-8")))