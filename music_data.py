import re
import time
import selenium_web as web
from selenium import webdriver

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
print(match_index,'\nimg:'+str(match_img))
print(match_music_ids,"\n共匹配%d首" % len(match_music_ids))

#抓取每首歌曲的1条评语，歌名
browser = webdriver.PhantomJS( )
browser.set_window_size(1120, 550)

i = 1
for song_id in match_music_ids:
      #延时5秒
      #time.sleep(5)
      #测试
      #if i > 5:
      #    break
      #拼接url
      song_url = r'http://music.163.com/#/song?id=%s' % song_id
      #此处不再调用web函数，有bug
      #song_data = web.get_web(song_url)
      browser.get(song_url)  
      browser.switch_to.frame(browser.find_element_by_xpath("//iframe"))
      #匹配评论&歌名
      ele_com = browser.find_element_by_xpath("//div[@class='cnt f-brk']")
      ele_name = browser.find_element_by_xpath("//em[@class='f-ff2']")
      print(i,song_id,ele_name.text,ele_com.text)
      #由于输出乱码问题所以不再使用网页源码+正则匹配数据
      #web_data = browser.page_source
      #song_data = web_data
      #检测网页
      #print(song_data, file=open('C:/Users/welwel/Desktop/%s.txt'%str(i) ,'a+',encoding='utf-8'))
      #构建评论&歌名正则
      #re_comment = r'class="s-fc7">(.*?)</a>.*?：(.*?)[</div>|<img ]'
      #re_songname = r'<em class="f-ff2">(.*?)</em>'
      #匹配数据
      #comment_data= re.findall(re_comment, song_data)
      #songname= re.findall(re_songname, song_data)
      #print(comment_data)
      #检验数据
      #song_all = str(songname) + '\n' + str(comment_data)
      #print(song_all, file=open('C:/Users/welwel/Desktop/song.txt' ,'a+',encoding='utf-8'))
      #测试使用
      i += 1
      #print(comment_data, file=open('C:/Users/welwel/Desktop/song.txt' ,'a+',encoding='utf-8'))
browser.quit();


