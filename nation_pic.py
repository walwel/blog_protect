#coding:utf-8
import re
import pymysql
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import urllib.request
from lxml import etree


#保存图片到本地
def savePicDate(url, pic_dir,pic_name):
      """将图片保存在本地"""
      f_pic = open(pic_dir+pic_name,'wb+')
      pic_data = urllib.request.urlopen(url).read()
      f_pic.write(pic_data)
      f_pic.close()
#连接数据库
def openDb():
      conn = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            port = 3306,
            db = 'blog',
            charset = 'utf8'
            )
      cur = conn.cursor()
      return conn,cur
#查询,创建表
def exeQuery(cur,conn,sql):
      cur.execute(sql)
      conn.commit()
      return (cur)
#关闭数据库
def connClose(cur,conn):
      cur.close()
      conn.close()

browser = webdriver.Chrome()
browser.get("http://www.nationalgeographic.com.cn/photography/photo_of_the_day/")
#保存文件路径
picPath = "E:/html模板/pic_data/nation_pic/"
#打开数据库
conn,cur = openDb()
pic_i = 1
#点击次数
for i in range(1,11):  
      eleget = browser.find_element_by_id("load-more")
      eleget.click()
      time.sleep(4)
      print(">>>>加载%s" % i)
html_data = browser.page_source
#关闭浏览器
browser.quit()
#print(html_data)
#print(html_data,file=open("C:/Users/welwel/Desktop/nation%s.html" % i, "a+",encoding='utf-8'))
#获取网页id
rnation = r'href="/photography/photo_of_the_day/(.*?).html"'
#print(len(html_data))
mnation = re.findall(rnation, html_data)
#print("mnation", mnation,len(mnation))
#去重排序
mnation = list(set(mnation))
mnation.sort()
print("mnation 111", mnation,len(mnation))
#浏览
url_header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'}
for url_id in mnation:
      #打开每个id
      pic_url = "http://www.nationalgeographic.com.cn/photography/photo_of_the_day/%s.html" % url_id
      print(">>>%s" % pic_url)
      req = urllib.request.Request(url=pic_url, headers=url_header)
      pic_html = urllib.request.urlopen(req)
      pic_data = pic_html.read()
      pic_data = pic_data.decode("utf-8")
      #print(pic_data,file=open("C:/Users/welwel/Desktop/pic_nation%s.html" % url_id, "a+",encoding='utf-8'))
      #url, title
      r_url = r'<li><div class="img-wrap"><a href="javascript:;" hidefocus="true"><img src="(.*?)" alt="(.*?)" rel'
      #infor
      r_infor = r'''<div class="public-p  m-p M-L-article del-bottom">(.*?)
[<|&]'''
      math_url = re.findall(r_url, pic_data)
      math_infor = re.findall(r_infor, pic_data)
      math_infor = re.sub(r'<.*?>','',math_infor[0])
      #print(math_url,math_infor) 图片url，title，information
      print(math_url,file=open("C:/Users/welwel/Desktop/na.txt" , "a+",encoding='utf-8'))
      print(math_infor,file=open("C:/Users/welwel/Desktop/nxa.txt" , "a+",encoding='utf-8'))
      #保存图片到本地
      picUrl = math_url[0][0]
      picName = url_id +'.jpg'
      savePicDate(picUrl, picPath, picName)
      #写入数据库 id, pic_id, pic_title, pic_infor, pic_urlid
      pic_id = picName
      pic_title = math_url[0][1]
      pic_infor = math_infor
      pic_urlid = url_id
      sql = "INSERT INTO blog_nation_pic VALUE (%d, '%s', '%s', '%s', '%s')" % (pic_i, pic_id, pic_title, pic_infor, pic_urlid)
      #cur,conn,sql
      exeQuery(cur, conn, sql)
      print('<<<成功写入第%d条' % pic_i)
      pic_i += 1













