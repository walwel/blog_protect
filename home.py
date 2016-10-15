import urllib.request
import re
url_html = "http://wufazhuce.com/"
url_header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0'}
req = urllib.request.Request(url=url_html, headers=url_header)
home_html = urllib.request.urlopen(req)
home_data = home_html.read()
home_data = home_data.decode("utf-8")

print('Status', home_html.status, home_html.reason)
for k, v in home_html.getheaders():
      print('%s:%s' % (k, v))
#print(home_data)
re_img = r'<img class="fp-one-imagen" src="(.*?)" alt'
re_zz = r"""<div class="fp-one-imagen-footer">
                            (.*?)                       </div>"""
re_word = r"""<div class="fp-one-cita">
                            <a href=".*?">(.*?)</a>                            </div>
"""
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
match_list = re.findall(re_img, home_data)
match_zz = re.findall(re_zz, home_data)
match_word = re.findall(re_word, home_data)
match_all = re.findall(re_all, home_data)

for l in match_all:
      print(l,'\n')


