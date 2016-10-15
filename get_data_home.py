#coding=utf-8
import pymysql
import urllib.request
import re

#连接数据库blog
def connDB():
      conn = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            port = 3306,
            db = 'blog',
            charset = 'utf8'
            )
      cur = conn.cursor()
      return conn,cur

#更新
def exeUpdate(cur,conn,sql):
      sta = cur.execute(sql)
      conn.commit()
      return sta;

#删除
def exeDelete(cur,IDs):
      for eachID in IDs.split(' '):
            sta=cur.execute('delete from blog where ')
      conn.commit()

#查询,创建表
def exeQuery(cur,conn,sql):
      cur.execute(sql)
      conn.commit()
      return (cur)
#关闭
def connClose(cur,conn):
      cur.close()
      conn.close()

#图片保存
def save_pic(url,pic_dir,pic_name):
      """将图片保存在本地"""
      f_pic = open(pic_dir+pic_name,'wb+')
      pic_data = urllib.request.urlopen(url).read()
      f_pic.write(pic_data)
      f_pic.close()
if __name__ == '__main__':
      try:
            conn, cur = connDB()
      except pymysql.Error as e:
            print('MySQLError : %d:%s' % (e.args[0], e.args[1]))
      print (conn,cur)
      
