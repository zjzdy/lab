# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 18:39:58 2018

@author: zjzdy
"""
import json
import urllib.request

yhm = b"your_id"
mm = b"your_password"
xn = "2017"
xq = "2"

# 获取课表json
request = urllib.request.Request("https://j.choyri.com/edu/schedule", b"{\"id\":\""+yhm+b"\",\"pwd\":\""+mm+b"\"}")
request.add_header('content-type', 'application/json')  # 设置POST数据类型
response = urllib.request.urlopen(request)
kb_json = json.loads(response.read())
print(kb_json)

# NoTry: http://120.55.151.61/V2/Course/getCourseTableFromSchool3.action