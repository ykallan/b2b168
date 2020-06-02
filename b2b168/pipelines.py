# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
pymysql.install_as_MySQLdb()

class B2B168Pipeline(object):

    def __init__(self):
        self.conn = pymysql.Connect(
            host='localhost',
            port=3306,
            database='scrapy',
            user='root',
            passwd='root',
            charset='utf8',
        )

        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        self.cursor.execute('''INSERT INTO b2b(com_name, hangye, gongyingchangjia, address, product, lianxiren, dianhua) VALUES(%s, %s, %s, %s, %s, %s, %s)''',
                            (item['com_name'], item['hangye'], item['gongyingchangjia'], item['address'], item['product'], item['lianxiren'], item['dianhua']))
        self.conn.commit()
        return item


    def close(self, spider):
        # self.cursor.close()
        # self.conn.close()
        pass