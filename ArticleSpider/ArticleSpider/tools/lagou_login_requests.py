#@Time  :   2018/5/22 11:33
#@Author:   zjl
#@File  :   lagou_login_requests.py.py
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

session = requests.session()

# 模仿浏览器请求
agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
header =  {
    # 主机地址
    "HOST": "www.lagou.com",
    "Referer": "https://www.lagou.com",
    'User-Agent': agent
}

# 判断是否登录
def is_login():
    inbox_url = "https://account.lagou.com/account/cuser/userInfo.html";
    # 不允许重定向，来判断是否可以访问只有登录用户才可以访问的页面
    response = session.get(inbox_url,headers = header, allow_redirects = False)
    if response.status_code != 200:
        return False
    else:
        return True

# 获取登录页
def login_page():
    response = requests.get("https://passport.lagou.com/login/login.html",headers = header)
    print(response.text)

# 返回首页状态
def get_index():
    response = session.get("https://www.zhihu.com",headers = header)
    with open("index_page.html","wb") as f:
        f.write(response.text.encode('UTF-8'))
    print('ok')

# 拉钩登录
def lagou_login(username,password):
    post_url = 'https://passport.lagou.com/login/login.json'
    post_data = {
        'isValidate': 'true',
        'password': password,
        'request_form_verifyCode': '',
        'submit': '',
        'username': username
    }
    response_text = session.post(post_url,data=post_data,headers = header)


login_page()
lagou_login('18202746477','e892cb171d6e823077a7b707efa4c7a5')
#get_index()
print(is_login())