#coding:utf-8
#获取豆瓣图书top250
import urllib.request
import pymysql
import re
import time

#获取网页
def getHtmlDate(url):
      urlHead = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'}
      req = urllib.request.Request(url=url, headers=urlHead)
      try:
            htmlDate = urllib.request.urlopen(req).read()
            htmlDate = htmlDate.decode('utf-8')
            #验证数据是否正确
            #print(htmlDate,file=open("C:/Users\welwel\Desktop\douban.html","a+",encoding="utf-8"))
            return htmlDate
      except :
            print("不存在 %s" %url )
            return "不存在"
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


#待爬取页
url = 'https://book.douban.com/top250?start='
picPath = "E:/html模板/pic_data/doubanBook/"
#打开数据库
conn,cur = openDb()
book_i = 1
#爬取页码为0,25,50,75,100...
for urlNum in range(0, 250, 25):
      urlFull = url + str(urlNum)
      #验证url是否正确
      print("正在爬取：%s" % urlFull)
      doubanDate = getHtmlDate(urlFull)
      #构造正则匹配 书ID, 书名，作者出版信息, 评分，图片
      reBookid = r'<a class="nbg" href="https://book.douban.com/subject/(.*?)/"'
      reBookname= r'&#34; title="(.*?)"'
      reBookin = r'<p class="pl">(.*?)</p>'
      reBookpinfen = r'<span class="rating_nums">(.*?)</span>'
      reBookpic = r'<img src="(.*?)" width="64" />'
      matchBookid = re.findall(reBookid,doubanDate)
      matchBookname = re.findall(reBookname,doubanDate)
      matchBookin = re.findall(reBookin,doubanDate)
      #由于图书信息包含 '[英] 伊恩·麦克尤恩 / 潘帕 / 南京大学出版社 / 2010-2 / 22.00元'
      matchBookpinfen = re.findall(reBookpinfen,doubanDate)
      matchBookpic = re.findall(reBookpic,doubanDate)
      books = [[a,b,c,d,e] for a,b,c,d,e in zip(matchBookid, matchBookname, matchBookin, matchBookpinfen, matchBookpic)]
      for book in books:
            #保存图片
            picUrl = book[4]
            picName = book[0] +'.jpg'
            #savePicDate(picUrl, picPath, picName)
            #为每本书加上简介和作者简介
            #匹配内容简介，作者简介
            reBookjianjie = r'''<div class="intro">
    <p>(.*?)</div>'''
            bookJianjieUrl = 'https://book.douban.com/subject/%s/' % book[0]
            print(">>>正在爬取：%s" % bookJianjieUrl)
            eachBookDate = getHtmlDate(bookJianjieUrl)
            #爬取内容简介，作者简介
            matchBookJianjie = re.findall(reBookjianjie,eachBookDate)
            if len(matchBookJianjie) >0:
                  if len(matchBookJianjie) >=2:
                        book.append(re.sub(r'<.*?>', '', matchBookJianjie[-2]))
                        book.append(re.sub(r'<.*?>', '', matchBookJianjie[-1]))
                  else:
                        book.append(re.sub(r'<.*?>', '', matchBookJianjie[-1]))
                        book.append("无作者简介")
            else :
                  book.append("无内容简介")
                  book.append("无作者简介")
            #写入数据库 id, book_name, book_intor, book_id, book_picurl, book_pic, book_infor, author_intor, book_pin
            book_pic = picName
            book_name = book[1]
            book_intor = book[5]
            book_id = book[0]
            book_picurl = book[4]
            book_infor = book[2]
            author_intor = book[6]
            book_pin = book[3]
            sql = "INSERT INTO blog_book VALUE (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (book_i, book_name, book_intor, book_id, book_picurl, book_pic, book_infor, author_intor, book_pin)
            #cur,conn,sql
            exeQuery(cur, conn, sql)
            #print(book, file=open("C:/Users\welwel\Desktop\dbook.txt","a+",encoding="utf-8"))
            print('<<<成功写入第%d条' % book_i)
            book_i += 1
connClose(cur,conn)
      














