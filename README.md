## t00ls自动签到脚本

### 流程分析

注：登陆前需要获取formhash，登陆后需要重新获取webhash，两个hash不同，否则会报错“您的请求来路不正确，无法提交”。

整个流程分为四步：获取formhash—>登陆并获取UTH_auth—>获取webhash—>签到

```
GET https://www.t00ls.net/logging.php?action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login
*{{formhash}}

POST https://www.t00ls.net/logging.php?action=login&loginsubmit=yes&floatlogin=yes&inajax=1
formhash=*{{formhash}}&referer=https%3A%2F%2Fwww.t00ls.net%2Findex.php&loginfield=username&username=xxx&password=md5(pass)&questionid=1&answer=xxx&cookietime=2592000
*{{cookie_UTH_auth}}

GET https://www.t00ls.net/members-profile-7807.html
Cookie: UTH_auth=*{{cookie_UTH_auth}}
*{{webhash}}

POST https://www.t00ls.net/ajax-sign.json
Cookie: UTH_auth=*{{cookie_UTH_auth}}&checkpm=1
formhash=*{{webhash}}&signsubmit=apply
```

### 定时器

设置定时任务：

```
crontab -e 或者直接编辑 vim /etc/crontab
// 设置每天3点执行脚本
0 3 * * * python /path/main.py
```
