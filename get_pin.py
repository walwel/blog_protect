from selenium import webdriver
import re
#匹配评论
#re_pin = r'<div class="cnt f-brk"><a href="/user/home?id=(.*?)" class="s-fc7">(.*?)</a>：(.*?)</div>'
#re_pin = r'<div class="cntwrap"><div class=""><div class="cnt f-brk"><a href="/user/home?id=(.*?)" class="s-fc7">(.*?)</a>(.*?)</div></div><div class="rp"><div class="time s-fc4">(.*?)</div><a data-id="(.*?)" data-type="like"'
re_pin = r'class="s-fc7">(.*?)</a>.*?：(.*?)[</div>|<img ]'
match_music = '428095913'
song_file = open('C:/Users/welwel/Desktop/%s.txt' % match_music,'r',encoding='utf-8')
song_data = song_file.read()
print(len(song_data))
#匹配数据
song_music = re.findall(re_pin,song_data)
print(song_music)





