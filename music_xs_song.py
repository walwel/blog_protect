import re
import time
import selenium_web as web
from selenium import webdriver
import save_data_db as db_save

#爬取的歌手主页
url = 'http://music.163.com/#/artist?id=5771'
#保存网页源码
web_data = web.get_web(url)
#检测数据是否抓取
#print(web_data)
#提取歌曲代码（50首）
#re_music = r'<div class="hd"><span data-res-id="(.*?)" data-res-type="18" data-res-action="play" data-res-from=".*?">'
re_music = r'<tr id=".*?" class=".*?"><td class="w1"><div class="hd"><span data-res-id="(.*?)" data-res-type="18" '
#匹配数据 歌曲id，歌手名&简介
match_music_ids = re.findall(re_music,web_data)
#检测数据是否匹配成功
#print(match_music_ids,"\n共匹配%d首" % len(match_music_ids))

print("开始连接数据库...")
#连接写入数据库
conn, cur = db_save.connDB()
print("连接数据库成功...")
#抓取每首歌曲的1条评语，歌名
browser = webdriver.PhantomJS( )
browser.set_window_size(1120, 550)

#写入数据库
m_id = 1
for song_id in match_music_ids:
      #拼接url
      song_url = r'http://music.163.com/#/song?id=%s' % song_id
      #此处不再调用web函数，有bug
      #song_data = web.get_web(song_url)
      browser.get(song_url)  
      browser.switch_to.frame(browser.find_element_by_xpath("//iframe"))
      #匹配评论&歌名
      ele_com = browser.find_element_by_xpath("//div[@class='cnt f-brk']")
      ele_name = browser.find_element_by_xpath("//em[@class='f-ff2']")
      #检测是否成功
      #print(i,song_id,ele_name.text,ele_com.text)
      music_id = song_id
      music_name = ele_name.text
      music_com = ele_com.text
      #开始写入m_id, music_id, music_name, music_com
      music_sql = "INSERT INTO blog_xs_music VALUES (%d, '%s', '%s', '%s')" % (m_id, music_id, music_name, music_com)
      db_save.exeQuery(cur,conn,music_sql)
      m_id += 1
browser.quit();
#关闭数据库
db_save.connClose(cur,conn)



