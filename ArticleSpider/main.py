#@Time  :   2018/4/10 21:10
#@Author:   zjl
#@File  :   main.py

from scrapy.cmdline import execute

import sys
import os

'''os.path.abspath(__file__)获取当前main文件的路径'''
'''os.path.dirname(file)得到file文件的父目录路径'''
print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# scrapy启动jobbole.py 命令为 scrapy crawl 文件名，所以使用数组保存这三个字符
# execute(["scrapy","crawl","jobbole"])
execute(["scrapy","crawl","zhihu"])