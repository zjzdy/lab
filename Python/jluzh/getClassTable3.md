# 吉珠课表获取(2)

---
## 前言 ##

    在未特殊说明情况下,代码默认为Python3代码

为了快一点,在[吉珠课表获取(2)](getClassTable2.md)中使用python自行模拟用户获取课程表,但其实最方便的是拾人牙慧来完成课程表的获取

我们要获取自己的课表,首先有2个变量是必须先知道的
 - 用户名(学号)
 - 密码(教务系统密码)

## 正戏 ##
0. 安装一些必要的东西
    1. 安装一个python环境

1. 先import必要的东西与定义那2个变量
    ```
    import json
    import urllib.request
    
    yhm = b"your_id"
    mm = b"your_password"
    ```
    
2. 获取课表json
    ```
	# 获取课表json
	request = urllib.request.Request("https://j.choyri.com/edu/schedule", b"{\"id\":\""+yhm+b"\",\"pwd\":\""+mm+b"\"}")
	request.add_header('content-type', 'application/json')  # 设置POST数据类型
	response = urllib.request.urlopen(request)
	kb_json = json.loads(response.read())
	print(kb_json)
    ```
    
## 效果 ##
略
