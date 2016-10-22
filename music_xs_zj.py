import re
import time
from selenium import webdriver
import save_data_db as db_save

#打开浏览器
browser = webdriver.PhantomJS( )
browser.set_window_size(1120, 550)
print("开始连接数据库...")
#连接写入数据库
conn, cur = db_save.connDB()
print("连接数据库成功...")
#打开图片文件夹
pic_dir = 'E:/html模板/pic_data/xs专辑图片/'
list_zj = ['0', '12']
zj_i = 1
for url in list_zj:
      #爬取的歌手专辑主页
      url = 'http://music.163.com/#/artist/album?id=5771&limit=12&offset=%s' % url
      #抓取第一页
      browser.get(url)  
      browser.switch_to.frame(browser.find_element_by_xpath("//iframe"))
      web_data = browser.page_source
      #检测数据是否抓取
      #print(web_data)
      #提取专辑名&照片url&专辑id
      re_zj = r"""<div class="u-cover u-cover-alb3" title="(.*?)">
<img src="(.*?)">
<a href="(.*?)" class="msk"></a>"""
      #匹配专辑
      match_zj = re.findall(re_zj,web_data)
      #检测数据是否匹配成功
      for zj in match_zj:
            #检测是否匹配成功
            #print(type(zj[0]), type(zj[1]), type(zj[2]))
            #写入图片(url,pic_dir,pic_name)
            url = zj[1]
            pic_name = "zj" + str(zj_i) + ".jpg"
            db_save.save_pic(url, pic_dir, pic_name)
            #写入id, zj_name, zj_pic, zj_id, zj_pic_id
            zj_name = zj[0]
            zj_pic = zj[1]
            zj_id = re.findall(r'id=(.*)', zj[2])[0]
            zj_pic_id = pic_name
            xs_zj_sql = "INSERT INTO blog_xs_zj VALUES (%d, '%s', '%s', '%s', '%s')" % (zj_i, zj_name, zj_pic, zj_id, zj_pic_id)
            print(xs_zj_sql)
            db_save.exeQuery(cur,conn,xs_zj_sql)
            zj_i += 1
#退出浏览器
browser.quit();
#关闭数据库
db_save.connClose(cur,conn)
