#@Time  :   2018/5/25 10:52
#@Author:   zjl
#@File  :   main.py

from scrapy.cmdline import execute

import sys
import os

# 当前文件的父目录的绝对路径，即最顶层目录
print(os.path.dirname(os.path.abspath(__file__)))

# 添加要搜索的目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 入口
# execute(["scrapy","crawl","lagou_sel"])
execute(["scrapy","crawl","zhihu_sel"])