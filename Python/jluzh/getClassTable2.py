# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 18:39:58 2018

@author: zjzdy
"""
import rsa
import base64
import json
import re
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar

yhm = "your_id"
mm = b"your_password"
xn = "2017"
xq = "2"

# 使用cookie
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
# 获取csrftoken
soup = BeautifulSoup(opener.open("http://jw.jluzh.com/xtgl/login_slogin.html").read(),'html.parser')
csrftoken = soup.find(id="csrftoken").get("value")
# 获取密码加密的rsa秘钥
key_json = json.loads(opener.open("http://jw.jluzh.com/xtgl/login_getPublicKey.html").read())
key = rsa.PublicKey(int.from_bytes(base64.b64decode(key_json["modulus"]), byteorder='big'), int.from_bytes(base64.b64decode(key_json["exponent"]), byteorder='big'))
# 构造登录POST所需的数据
mm_base64 = base64.b64encode(rsa.encrypt(mm, key))
values = {'csrftoken': csrftoken, 'yhm': yhm, "mm": mm_base64}
data = urllib.parse.urlencode(values).encode(encoding='UTF8')
# 登录并获取gnmkdm
req = urllib.request.Request("http://jw.jluzh.com/xtgl/login_slogin.html", data)
res = opener.open(req)
gnmkdm = re.search("clickMenu.'(\S*)','(\S+)','学生课表查询'",res.read().decode('utf-8')).group(1)
# 获取学期所对应的值
soup = BeautifulSoup(opener.open("http://jw.jluzh.com/kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N253508").read(),'html.parser')
xqm = soup.find(id="xqm1").find(text=xq).parent.get("value")
# 获取课表json
values = {'xnm': xn, 'xqm': xqm}
data = urllib.parse.urlencode(values).encode(encoding='UTF8')
req = urllib.request.Request("http://jw.jluzh.com/kbcx/xskbcx_cxXsKb.html?gnmkdm="+gnmkdm, data)
kb_json = json.loads(opener.open(req).read())
print(kb_json)
# 获取课表PDF
req = urllib.request.Request("http://jw.jluzh.com/kbcx/xskbcx_cxXsShcPdf.html?doType=table&xnm="+xn+"&xqm="+xqm+"&xszd.sj=true&xszd.cd=true&xszd.js=true&xszd.jszc=false&xszd.jxb=true&xnmc="+xn+"&xqmmc="+xq+"&xm=&jgmc=&xxdm=&xh="+yhm+"&xh_id="+yhm+"&gnmkdm="+gnmkdm)
res = opener.open(req)
# 写入课表PDF
f = open(yhm + '-' + xn + '-' + xq + '.pdf', 'wb')
f.write(res.read())
f.close()