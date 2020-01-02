#!/usr/bin/env python
# -*- coding: utf-8 -*-

__Author__ = "SewellDing"

import hashlib
import re
import requests

session = requests.session()


# 获取登录窗口页面的formhash
def get_formhash():
    url = "https://www.t00ls.net/logging.php?action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login"
    headers = {"Host": "www.t00ls.net",
               "Connection": "keep-alive",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
               "X-Requested-With": "XMLHttpRequest",
               "Accept": "application/json, text/javascript, */*; q=0.01",
               "Referer": "https://www.t00ls.net/index.php",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh,zh-CN;q=0.9,en;q=0.8"}
    session.headers.clear()
    session.headers.update(headers)
    resp = session.get(url)
    # 获取formhash
    p = resp.text.find("formhash") + len("formhash' value='")
    formhash = resp.text[p:p + 8]
    return formhash


# 模拟登录并返回Cookie
def login(formhash, username, password, questionid, answer):
    url = "https://www.t00ls.net/logging.php?action=login&loginsubmit=yes&floatlogin=yes&inajax=1"
    data = {
        "formhash": formhash,
        "referer": "https://www.t00ls.net/index.php",
        "loginfield": "username",
        "username": username,
        "password": password,
        "questionid": questionid,
        "answer": answer,
        "cookietime": 2592000
    }
    headers = {"Host": "www.t00ls.net",
               "Connection": "keep-alive",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
               "X-Requested-With": "XMLHttpRequest",
               "Accept": "application/json, text/javascript, */*; q=0.01",
               "Referer": "https://www.t00ls.net/index.php",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh,zh-CN;q=0.9,en;q=0.8"}
    session.headers.clear()
    session.headers.update(headers)
    resp = session.post(url, data)
    content = resp.text
    # print("resp.content:\n", content)
    expression = r"<p>(.*)</p>"
    welcome = re.findall(expression, content)
    print("Welcome title:", welcome[0])
    # print(resp.cookies["UTH_auth"])
    return resp.cookies["UTH_auth"]


# 获取签到页面的webhash
def get_webhash(cookie):
    url = "https://www.t00ls.net/members-profile-7807.html"
    headers = {"Host": "www.t00ls.net",
               "Connection": "keep-alive",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
               "X-Requested-With": "XMLHttpRequest",
               "Accept": "application/json, text/javascript, */*; q=0.01",
               "Referer": "https://www.t00ls.net/index.php",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh,zh-CN;q=0.9,en;q=0.8"}
    session.headers.clear()
    session.headers.update(headers)
    cookies = {"UTH_auth": cookie}
    resp = session.get(url, cookies=cookies)
    # 获取webhash
    p = resp.text.find("WebSign") + len("WebSign('")
    webhash = resp.text[p:p + 8]
    return webhash

# 签到
def automatic_checkin(webhash, cookie_UTH_auth):
    url = "https://www.t00ls.net/ajax-sign.json"
    data = {
        "formhash": webhash,
        "signsubmit": "apply"
    }
    headers = {"Host": "www.t00ls.net",
               "Connection": "keep-alive",
               "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
               "X-Requested-With": "XMLHttpRequest",
               "Accept": "application/json, text/javascript, */*; q=0.01",
               "Referer": "https://www.t00ls.net/members-profile-7807.html",
               "Origin": "https://www.t00ls.net",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               "Content-Length": "34",
               "Sec-Fetch-Site": "same-origin",
               "Sec-Fetch-Mode": "cors",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh,zh-CN;q=0.9,en;q=0.8",
               }
    session.headers.clear()
    session.headers.update(headers)
    cookies = {"UTH_auth": cookie_UTH_auth, "checkpm": "1"}
    resp = session.post(url, data, cookies=cookies)
    content = resp.text
    print("resp.content:", content)


def get_md5(string):
    m5 = hashlib.md5()
    m5.update(string)
    return m5.hexdigest()


def main():
    formhash = get_formhash()
    print("[+] formhash:" + formhash)
    username = "用户名"
    print("[+] username:" + username)
    password = get_md5("密码".encode("utf-8"))
    print("[+] password:" + password)
    q = {"0": "安全提问(未设置请忽略)", "1": "母亲的名字", "2": "爷爷的名字", "3": "父亲出生的城市", "4": "您其中一位老师的名字", "5": "您个人计算机的型号",
         "6": "您最喜欢的餐馆名称", "7": "驾驶执照最后四位数字"}
    questionid = "问题编号"
    print("[+] question:" + q.get(questionid))
    answer = "问题答案"
    print("[+] answer:" + answer)
    cookie_UTH_auth = login(formhash, username, password, questionid, answer)
    webhash = get_webhash(cookie_UTH_auth)
    automatic_checkin(webhash, cookie_UTH_auth)


if __name__ == "__main__":
    main()
