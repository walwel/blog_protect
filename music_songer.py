import re
import time
import selenium_web as web
from selenium import webdriver
import save_data_db as db_save

#爬取歌手主页
url = 'http://music.163.com/#/discover/artist'
#保存网页源码
web_data = web.get_web(url)
#检测数据是否抓取
#print(web_data)
#提取歌手图片url[0]，名[1]，id[2]
re_songer = r"""<li.*?><div class="u-cover u-cover-5"><img src="(.*?)"><a title="(.*?)的音乐" href="(.*?)" class="msk"></a></div>"""
match_songer = re.findall(re_songer, web_data)
#检测数据是否匹配成功
print(match_songer)
#打开图片文件夹
pic_dir = 'E:/html模板/pic_data/songer_img/'
song_i = 1
print("开始连接数据库...")
#连接写入数据库
conn, cur = db_save.connDB()
print("连接数据库成功...")
for songer in match_songer:
      #写入图片(url,pic_dir,pic_name)
      url = songer[0]
      pic_name = "songer" + str(song_i) +".jpg"
      db_save.save_pic(url, pic_dir, pic_name)
      #写入id, songer_name, songer_pic, songer_pic_id, songer_id
      songer_name = songer[1]
      songer_pic = songer[0]
      songer_pic_id = pic_name
      songer_id = re.findall(r'.*?id=(.*)', songer[2])[0]
      songer_sql = "INSERT INTO blog_songer VALUES (%d, '%s', '%s', '%s', '%s')" % (song_i, songer_name, songer_pic, songer_pic_id, songer_id)
      db_save.exeQuery(cur,conn,songer_sql)
      song_i += 1
#关闭数据库
db_save.connClose(cur,conn)
