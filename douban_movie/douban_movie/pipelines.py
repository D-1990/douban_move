# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class DoubanMoviePipeline(object):
    def __init__(self):
        self.mysql_conn =pymysql.Connect(
            host='localhost',
            port=3306,
            user='root',
            password='12345',
            database='douban_movie',
            charset='utf8',
        )
    def process_item(self, item, spider):
        cs = self.mysql_conn.cursor()
        sql_column =','.join([key for key in item.keys()])
        sql_value = ','.join(['"%s"' %item[key] for key in item.keys()])
        sql = 'insert into douban_movie_top (%s) value (%s);' % (sql_column,sql_value)
        cs.execute(sql)
        self.mysql_conn.commit()
        return item
