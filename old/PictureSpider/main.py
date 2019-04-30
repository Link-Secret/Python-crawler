#@Time  :   2018/4/27 10:18
#@Author:   zjl
#@File  :   main.py

from scrapy.cmdline import execute

import sys
import os

print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# a = 'st'
# if a is 'st':
#     print('st')

# 启动
execute(["scrapy","crawl","meizitu"])
