import pymysql
conn = \
pymysql.connect(host='127.0.0.1',unix_socket='/tmp/mysql.sock',user='root',password='root',db='mysql',charset='utf8')

cur = conn.cursor()
cur.execute('USE footballSpider')

cur.execute('SELECT * FROM pages ')
url="http://google.com"
title="谷歌"
cur.execute("INSERT INTO pages (url,title,parsed) VALUES(%s,%s,1)",(url,title))
conn.commit()
print(cur.lastrowid)
cur.close()
conn.close()
