# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import copy
from pymysql import cursors
from twisted.enterprise import adbapi
import os
import sys
from .items import CallBidItem, WinBidItem

class BuildingSpiderPipeline(object):

    # 初始化函数
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 从settings配置文件中读取参数
    @classmethod
    def from_settings(cls, settings):
        # 用一个db_params接收连接数据库的参数
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset='utf8',
            use_unicode=False,
            # 设置游标类型
            cursorclass=cursors.DictCursor
        )
        # 创建连接池
        db_pool = adbapi.ConnectionPool('pymysql', **db_params)
        # 返回一个pipeline对象
        return cls(db_pool)

    def process_item(self, item, spider):
        if isinstance(item,CallBidItem):
            # 把要执行的sql放入连接池
            asynItem = copy.deepcopy(item)
            query = self.db_pool.runInteraction(self.insert_into_callbidsql, asynItem)
            # 如果sql执行发送错误,自动回调addErrBack()函数
            query.addErrback(self.handle_error, item, spider)
            # 返回Item
            return item

        elif isinstance(item,WinBidItem):
            # 把要执行的sql放入连接池
            asynItem = copy.deepcopy(item)
            query = self.db_pool.runInteraction(self.insert_into_winbidsql, asynItem)
            # 如果sql执行发送错误,自动回调addErrBack()函数
            query.addErrback(self.handle_error, item, spider)
            # 返回Item
            return item

    def insert_into_callbidsql(self, cursor, item):
        sql = 'INSERT INTO callbidsql (' + ','.join(item.keys()) + ') VALUES (' + ','.join(['%s'] * len(item)) + ')'
        # 执行sql语句
        cursor.execute(sql, tuple(item.values()))

    def insert_into_winbidsql(self, cursor, item):
        sql = 'INSERT INTO winbidsql (' + ','.join(item.keys()) + ') VALUES (' + ','.join(['%s'] * len(item)) + ')'
        # 执行sql语句
        cursor.execute(sql, tuple(item.values()))

    def handle_error(self, failure, item, spider):
        # #输出错误信息
        print(failure)
        print('爬虫bug结束')
        os._exit(0)


