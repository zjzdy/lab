# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 21:17:58 2018

@author: zjzdy
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import urllib.request
import urllib.error
import time

yhm = "your_id"
mm = "your_password"
xn = "2017"
xq = "2"
options = webdriver.ChromeOptions()
# 无头模式
options.add_argument('headless')
# 设置中文语言
options.add_argument('lang=zh_CN.UTF-8')
# 禁用图片
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
# 启动Chrome
browser = webdriver.Chrome("chrome/chromedriver", chrome_options=options)
# 设置内置等待时间
browser.implicitly_wait(2)
browser.get("http://jw.jluzh.com")
# 登录
browser.find_element_by_id('yhm').send_keys(yhm)
browser.find_element_by_id('mm').send_keys(mm)
time.sleep(0.3)
browser.find_element_by_id('dl').click()
time.sleep(1)

try:
    # 切换到课表查询页面
    browser.find_element_by_xpath("//a[contains(text(),'选课')]").click()
    browser.find_element_by_xpath("//a[contains(@onclick,'xskbcx_cxXskbcxIndex')]").click()
    browser.switch_to.window(browser.window_handles[1])
    print('Login Successful')
except NoSuchElementException:
    tips = browser.find_element_by_id('tips')
    print('Login Fail '+tips.text)
    browser.quit()
    exit(-1)

# 查询课表
browser.execute_script("$('#xnm1').val('" + xn + "');$('#xqm1').find(\"option:contains('" + xq + "')\").attr(\"selected\",true);searchResult1();")
try:
    # 检查课表是否存在
    tips = browser.find_element_by_id('kblist_table')
except NoSuchElementException:
    print('No Class Table')
else:
    # 重写openWin函数以获得课表PDF链接
    browser.execute_script("$.openWin = function func(url){$.PDF_URL = url;};")
    browser.find_element_by_id('shcPDF').click()
    pdf = browser.execute_script("return 'http://jw.jluzh.com'+$.PDF_URL")
    try:
        # 下载课表PDF
        request = urllib.request.Request(pdf)
        request.add_header('Cookie', 'JSESSIONID=' + browser.get_cookie('JSESSIONID')["value"])  # 设置cookie
        response = urllib.request.urlopen(request)
    except urllib.error.URLError:
        print('Download Fail')
    else:
        try:
            # 写入课表PDF
            f = open(yhm + '-' + xn + '-' + xq + '.pdf', 'wb')
            f.write(response.read())
            f.close()
        except IOError:
            print('Write Fail')
        else:
            print('Get Successful')
finally:
    browser.quit()
