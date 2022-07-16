# -*- coding: utf-8 -*- 
# @Time : 2022/7/15 9:21 
# @Author : 任浩天
# @File : SQL_create_Database.py
# 创建数据库
import pymysql
from SQL.configure import *

def create_Database():
    mydb = pymysql.connect(host=host,
                           user=user,
                           password=password,
                           charset='utf8'
                           )
    cursor = mydb.cursor()
    cursor.execute("create database CS_show")  # 创建数据库
    mydb.close()
    mydb.commit()


def create_table():
    mydb = pymysql.connect(host=host,
                           user=user,
                           password=password,
                           database='CS_show',
                           charset='utf8'
                           )
    cursor = mydb.cursor()
    cursor.execute("create table sys_name")  # 创建数据库
    cursor.execute("create table player_name")  # 创建数据库
    mydb.close()
    mydb.commit()


create_Database()
create_table()
