# -*- coding: utf-8 -*- 
# @Time : 2022/7/13 9:26 
# @Author : 任浩天
# @File : SQL_name.py

# 得到数据库中人名
import pymysql
from SQL.configure import *


class SQL_name:
    def __init__(self):
        self.name = []
        self.get_name_from_mysql()

    def get_name_from_mysql(self):
        db = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             database='cs_show',
                             charset='utf8')

        cursor = db.cursor()
        sql = "select * from sys_name;"
        cursor.execute(sql)
        data = cursor.fetchall()
        db.close()
        for i in data:
            self.name.append(i[0])
