#coding:utf-8
#获取豆瓣电影top250
import urllib.request
import pymysql
import re
import time
from lxml import etree

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
            return "0"
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
url = 'https://movie.douban.com/top250?start=%s&filter='
picPath = "E:/html模板/pic_data/doubanMovie/"
#打开数据库
conn,cur = openDb()
movie_i = 1
#爬取页码为0,25,50,75,100...
for urlNum in range(0, 250, 25):
      urlFull = url % str(urlNum)
      #验证url是否正确
      print("正在爬取：%s" % urlFull)
      doubanDate = getHtmlDate(urlFull)
      #电影url, 片名
      reMovieId= r'''<div class="hd">
                        <a href="(.*?)" class="">
                            <span class="title">(.*?)</span>'''
      #导演等信息
      reMovieIn = r'''<div class="bd">
                        <p class="">
                            (.*?)<br>
                            (.*?)
                        </p>'''
      #电影ID，片名，配图
      reMoviePic = r'''<a href="https://movie.douban.com/subject/.*?/">
                        <img alt=".*?" src="(.*?)" class="">'''
      #电影评分，短评
      reMoviepin = r'''<span class="rating_num" property="v:average">(.*?)</span>
                                <span property="v:best" content="10.0"></span>
                                <span>.*?</span>
                        </div>

                            <p class="quote">
                                <span class="inq">(.*?)</span>'''
      matchMovieId = re.findall(reMovieId,doubanDate)
      #print(matchMovieId)
      matchMovieIn = re.findall(reMovieIn,doubanDate)
      #print(matchMovieIn)
      matchMoviePic = re.findall(reMoviePic,doubanDate)
      #print(matchMoviePic)
      matchMoviepin = re.findall(reMoviepin,doubanDate)
      #print(matchMoviepin)
      #合并: 配图url，评分，短评，影片url，片名，导演等，影片类型时间；
      movies1 = [[a,d[0],d[1]] for a,d in zip(matchMoviePic,  matchMoviepin)]
      movies2 = [[a[0], a[1],d[0], d[1]] for a,d in zip(matchMovieId,  matchMovieIn)]
      movies = [[a+b] for a, b in zip(movies1, movies2)]
      #验证数据
      for movie in movies :
            movie = movie[0]
            #print(ma)
            #保存图片
            picUrl = movie[0]
            picName = str(movie_i) +'.jpg'
            savePicDate(picUrl, picPath, picName)
            #电影简介
            reMovieinfor = r'''<span property="v:summary">
                                    　　(.*?)
                                        <'''
            print(">>>正在爬取：%s" % picUrl)
            movieurl = movie[3]
            #使用xpath匹配数据
            movieDate = getHtmlDate(movieurl)
            if movieDate != "0":
                  tree = etree.HTML(movieDate)
                  #matchMovieinfor = re.findall(reMovieinfor,movieDate)
                  node = tree.xpath("//span[@property='v:summary']")
                  #print(node[0].text)
                  matchMovieinfor = node[0].text.replace("'",".")
                  #print(matchMovieinfor)
            else:
                  matchMovieinfor = "暂无信息"
            if len(matchMovieinfor) == 0:
                  print("==============%s 未获得数据" % movieurl )
                  break
            #合并 配图url，评分，短评，影片url，片名，导演等，影片类型时间，内容简介；
            movie.append(matchMovieinfor)
            #print(movie[7],len(movie))
            #写入数据库 id, movie_picurl, movie_picid, movie_pin, movie_Sintor, movie_url, movie_name, movie_author, movie_infor, movie_Lintor
            movie_picurl = movie[0]
            movie_picid = picName
            movie_pin = movie[1]
            movie_Sintor = movie[2].replace("'",".")
            movie_url = movie[3]
            movie_name = movie[4].replace("'",".")
            movie_author = movie[5].replace("'",".")
            movie_infor = movie[6].replace("'",".")
            movie_Lintor = movie[7]
            #print(movie_Lintor)
            sql = "INSERT INTO blog_movie VALUE (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                  (movie_i, movie_picurl,movie_picid, movie_pin, movie_Sintor, movie_url, movie_name, movie_author, movie_infor, movie_Lintor)
            #cur,conn,sql
            exeQuery(cur, conn, sql)
            print('<<<成功写入第%d条' % movie_i)
            movie_i += 1
connClose(cur,conn)
            














