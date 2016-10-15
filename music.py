from selenium import webdriver
import re
#打开浏览器
browser = webdriver.PhantomJS( )
browser.set_window_size(1120, 550)
#提取歌手名，简介
re_index = r"""<meta charset="utf-8">
<meta property="qc:admins" content=".*?">
<meta name="keywords" content="(.*?)">
<meta name="description" content="(.*?)
">"""
#提取歌曲代码（50首）
#re_music = r'<div class="hd"><span data-res-id="(.*?)" data-res-type="18" data-res-action="play" data-res-from=".*?">'
re_music = r'<tr id=".*?" class=".*?"><td class="w1"><div class="hd"><span data-res-id="(.*?)" data-res-type="18" '
#打开，读取网页源文件
music_file = open('C:/Users/welwel/Desktop/source.txt','r',encoding='utf-8')
music_data = music_file.read()
#匹配数据
#match_music = re.findall(re_music,music_data)
match_index = re.findall(re_index,music_data)
#song_num songer_index
print(match_index)
#print(match_music,end='', file=open('C:/Users/welwel/Desktop/blog_protect/song_num.txt','a+'))
#song_url
song_url = r'http://music.163.com/#/song?id=%s' % match_music[0]
# 打开网页
#browser.get(song_url)  
#browser.switch_to.frame(browser.find_element_by_xpath("//iframe"))
#保存源代码
#print(browser.page_source,file=open('C:/Users/welwel/Desktop/%s.txt' % match_music[0],'w',encoding='utf-8'))
#匹配评论
#browser.quit()




