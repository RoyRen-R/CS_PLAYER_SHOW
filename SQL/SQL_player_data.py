# -*- coding: utf-8 -*- 
# @Time : 2022/7/15 14:30 
# @Author : 任浩天
# @File : SQL_player_data.py

# 得到数据库中的player_data
# 数据库连接对象
import pymysql
from SQL.configure import *

class player_data:
    def __init__(self):
        self.data = get_data()

def get_data():
    conn = pymysql.connect(host=host, user=user, password=password, db="cs_show")
    # 游标对象
    cur = conn.cursor()
    # 查询的sql语句
    sql = "SELECT * FROM player_data"
    cur.execute(sql)
    # 获取查询到的数据, 是以二维元组的形式存储的, 所以读取需要使用 data[i][j] 下标定位
    data = cur.fetchall()
    conn.close()
    return data
