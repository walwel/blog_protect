#coding=utf-8
import save_data_db as db_save
import re
import time
from selenium import webdriver

#爬取的飙升主页
url = 'http://music.163.com/#/discover/toplist'
#开始抓取
browser = webdriver.PhantomJS( )
browser.set_window_size(1120, 550)
browser.get(url)  
browser.switch_to.frame(browser.find_element_by_xpath("//iframe"))
#保存抓取的网页
web_data = browser.page_source
browser.quit();
#抓取music_id,  music_name,  music_author, music_pic
re_music = r'title="收藏"></span><span data-res-id="(.*?)" data-res-type="18" data-res-action="share" data-res-name="(.*?)" data-res-author="(.*?)" data-res-pic="(.*?)" class="icn icn-share" title="分享">分享</span>'
match_musics = re.findall(re_music,web_data)
#将抓取的数据保存至文件
#print(match_musics, file=open('C:/Users\welwel\Desktop\music.txt','a+',encoding='utf-8'))
print("开始连接数据库...")
#连接写入数据库
conn, cur = db_save.connDB()
print("连接数据库成功...")
#写入数据库
m_id = 1
print("开始写入...")
#打开图片文件夹
pic_dir = 'E:/html模板/pic_data/up_img/'
for music in match_musics:
      #拼接url
      #song_url = r'http://music.163.com/#/song?id=%s' % music[0]
      #此处不再调用web函数，有bug
      #song_data = web.get_web(song_url)
      #browser.get(song_url)  
      #browser.switch_to.frame(browser.find_element_by_xpath("//iframe"))
      #匹配评论
      #ele_com = browser.find_element_by_xpath("//div[@class='cnt f-brk']/img[not(@src)] and sup[not(@class)]]")
      #music_id,  music_name,  music_author, music_pic， music_com, music_pic_id
      music_id = str(music[0])
      music_name = music[1].replace("'", ".")
      music_author = music[2].replace("'", ".")
      music_pic = music[3]
      music_pic_id = "up_img" + str(m_id) + '.jpg'
      #music_com = re.sub(r'<img src=".*?">', '', ele_com.text)
      #print(music_com)
      #将图片保存至本地
      #写入图片(url,pic_dir,pic_name)
      url = music_pic
      pic_name = music_pic_id
      db_save.save_pic(url, pic_dir, pic_name)
      #开始写入
      sql = "INSERT INTO blog_up_music VALUES (%d, '%s', '%s', '%s', '%s', '%s')" % (m_id, music_id, music_name, music_author, music_pic, music_pic_id)
      db_save.exeQuery(cur,conn,sql)
      m_id += 1
print("写入成功...")

#关闭数据库
db_save.connClose(cur,conn)

      
