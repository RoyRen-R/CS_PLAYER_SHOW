# -*- coding: utf-8 -*- 
# @Time : 2022/7/15 9:10 
# @Author : 任浩天
# @File : SQL_insertdata.py

# 将palyer_data的数据传入数据库中
import pandas as pd
from sqlalchemy import create_engine
from SQL.configure import *

# 读取数据
data_player = pd.read_csv('player_data.csv', encoding='gbk')
columns = ['ID', 'KAST', 'IMPACT', 'RATING', 'Total_kills', 'Headshot', 'Total_deaths', 'KD_Ratio',
           'Damage_Round', 'Grenade_dmg_Round', 'Maps_played', 'Rounds_played'
    , 'Kills_round', 'Assists_round', 'Deaths_round', 'Saved_by_teammate_round', 'Saved_teammates_round']
data_player.columns = columns  # 修改可存入数据库中列名
ls_name = ls_name
data_name = pd.DataFrame(ls_name, columns=['stu_name'])


# 构建读入数据库的类
class PDTOMYSQL:
    def __init__(self, host, user, password, db, tb, df, port='3306'):
        self.host = host
        self.user = user
        self.port = port
        self.db = db
        self.password = password
        self.tb = tb
        self.df = df

        sql = 'select * from ' + self.tb
        conn = create_engine(
            'mysql+pymysql://' + self.user + ':' + self.password + '@' + self.host + ':' + self.port + '/' + self.db)
        df.to_sql(self.tb, con=conn, if_exists='replace', index=False)
        self.pdata = pd.read_sql(sql, conn)

    def show(self):  # 显示数据集
        return print(self.pdata)


t = PDTOMYSQL(host=host, user=user, password=password, db='cs_show', tb='player_data', df=data_player)
t2 = PDTOMYSQL(host=host, user=user, password=password, db='cs_show', tb='sys_name', df=data_name)
