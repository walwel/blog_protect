#coding=utf-8
import urllib.request
import re
import get_data_home

url_html = "http://wufazhuce.com/"
url_header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'}
req = urllib.request.Request(url=url_html, headers=url_header)
home_html = urllib.request.urlopen(req)
home_data = home_html.read()
home_data = home_data.decode("utf-8")

#print('Status', home_html.status, home_html.reason)
#for k, v in home_html.getheaders():
#      print('%s:%s' % (k, v))
#print(home_data)

#获取图片
re_img = r'<img class="fp-one-imagen" src="(.*?)" alt'
#match_list = re.findall(re_img, home_data)

#获取作者
re_zz = r"""<div class="fp-one-imagen-footer">
                            (.*?)                       </div>"""
#match_zz = re.findall(re_zz, home_data)

#获取名言
re_word = r"""<div class="fp-one-cita">
                            <a href=".*?">(.*?)</a>                            </div>
"""
#match_word = re.findall(re_word, home_data)

#获取全部
re_all = r"""<a href=".*?"><img class="fp-one-imagen" src="(.*?)" alt="" /></a>                        <div class="fp-one-imagen-footer">
                            (.*?)                        </div>
                        <div class="fp-one-cita-wrapper">
                            <div class="fp-one-titulo-pubdate">
                                <p class="titulo">.*?</p>
                                <p class="dom">.*?</p>
                                <p class="may">.*?</p>
                            </div>
                            <div class="fp-one-cita">
                            <a href=".*?">(.*?)<"""
match_all = re.findall(re_all, home_data)
#连接写入数据库,保存图片
conn, cur = get_data_home.connDB()
#打开图片文件夹
pic_dir = 'E:/html模板/pic_data/'
pic_num = 1
for each_data in match_all:
      #写入图片的作者
      #写入图片的名字
      #写入名句
      #rhesis, author, picture_name
      #print(each_data[2],'\n',each_data[1])
      #print(type(each_data[2]),'\n',type(each_data[1]))
      pic_name = str(pic_num) + '.' +'jpg'
      #写入图片(url,pic_dir,pic_name)
      get_data_home.save_pic(each_data[0], pic_dir, pic_name)
      sql = "INSERT INTO blog_home VALUES (%d,'%s','%s','%s')" % (pic_num,each_data[2],each_data[1],pic_name)
      print(sql)
      get_data_home.exeQuery(cur,conn,sql)
      pic_num += 1
get_data_home.connClose(cur,conn)

            

      


