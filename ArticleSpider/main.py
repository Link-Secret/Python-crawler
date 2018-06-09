#@Time  :   2018/4/10 21:10
#@Author:   zjl
#@File  :   main.py

from scrapy.cmdline import execute

import sys
import os

'''os.path.abspath(__file__)获取当前main文件的路径'''
'''os.path.dirname(file)得到file文件的父目录路径'''
print(os.path.dirname(os.path.abspath(__file__)))
# 当我们试图加载一个模块时，Python会在指定的路径下搜索对应的.py文件，如果找不到，就会报错

# 默认情况下，Python解释器会搜索当前目录、(ArticleSpider/ArticleSpider)
# 所有已安装的内置模块和第三方模块，搜索路径存放在sys模块的path变量中
# 
# 如果我们要添加自己的搜索目录，有两种方法：
# 一是直接修改sys.path，添加要搜索的目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# scrapy启动jobbole.py 命令为 scrapy crawl 文件名，所以使用数组保存这三个字符
#execute(["scrapy","crawl","jobbole"])
execute(["scrapy","crawl","zhihu_sel3"])
#execute(["scrapy","crawl","lagou_sel"])