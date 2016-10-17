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
#提取歌手名[0]，简介[1]
re_index = r"""<meta charset="utf-8">
<meta property="qc:admins" content=".*?">
<meta name="keywords" content="(.*?)">
<meta name="description" content="(.*?)
">"""
#提取照片
re_img = r"""</h3>
</div>
<img src="(.*?)">
<div class="mask f-alpha"></div>"""
#提取歌曲代码（50首）
#re_music = r'<div class="hd"><span data-res-id="(.*?)" data-res-type="18" data-res-action="play" data-res-from=".*?">'
re_music = r'<tr id=".*?" class=".*?"><td class="w1"><div class="hd"><span data-res-id="(.*?)" data-res-type="18" '
#匹配数据 歌曲id，歌手名&简介
match_music_ids = re.findall(re_music,web_data)
match_index = re.findall(re_index,web_data)
match_img = re.findall(re_img,web_data)
#检测数据是否匹配成功
#print(match_index,'\nimg:'+str(match_img))
#print(match_music_ids,"\n共匹配%d首" % len(match_music_ids))

print("开始连接数据库...")
#连接写入数据库
conn, cur = db_save.connDB()
print("连接数据库成功...")
#写入id, xs_name, xs_index, xs_img
xs_name = match_index[0][0]
xs_index = match_index[0][1]
xs_img = match_img[0]
xs_sql = "INSERT INTO blog_xs VALUES (%d, '%s', '%s', '%s')" % (1, xs_name, xs_index, xs_img)
db_save.exeQuery(cur,conn,xs_sql)
#关闭数据库
db_save.connClose(cur,conn)
