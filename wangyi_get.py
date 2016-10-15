from selenium import webdriver
import re

browser = webdriver.PhantomJS( )
#爬取的歌手主页
url = 'http://music.163.com/#/artist?id=5771'
# 打开网页
browser.get(url)  
browser.switch_to.frame(browser.find_element_by_xpath("//iframe"))
#保存网页源码
print(browser.page_source,file=open('C:/Users/welwel/Desktop/source.txt','w',encoding='utf-8'))
browser.quit()
#获取歌曲id，专辑
#music_html = open('C:/Users/welwel/Desktop/source.html','r',)
#music_data = music_html.decode("utf-8")
#re_music = r'<a href="/song?id=(.*?)"><b title="(.*?)">(.*?)</b>'
#
#for each_music in match_all:
#      print(each_music)

