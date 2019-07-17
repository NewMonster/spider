#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@Software: PyCharm
@Author  : cn
@Email   : chenningxj@163.com
@File    : db_helper.py
@Time    : 2019-7-16 下午3:50
@version : v1.0
"""
import pymysql

class DB_Connection(object):
    def __init__(self):
        self.conn=None
        self._open()


    def _open(self):
        try:
            self.conn=pymysql.connect(host='localhost',user='root',password='123456',database='airticket',charset="utf8")
        except Exception:
            raise NotImplementedError

    # 获取城市信息
    def get_city(self, city):
        cursor = self.conn.cursor()
        sql='select * from xiecheng where city="%s"'%city
        try:
            cursor.execute(sql)
            data = cursor.fetchone()
            return data
        except Exception as e:
            print(e)
            return None
        finally:
            cursor.close()


    # 添加城市信息
    def add_city(self, city, code, sign):
        cursor = self.conn.cursor()
        sql='insert into xiecheng(city,code,sign) values("%s",%d,"%s");'%(city,code,sign)
        try:
            data=cursor.execute(sql)
            self.conn.commit()
            return data
        except Exception as e:
            print(e)
            return None
        finally:
            cursor.close()


    # 保存航班信息
    def save_trip(self):
        pass


    # 根据条件获取航班信息
    def get_trip(self,where):
        pass


    # 根据排序字段获取排序后航班信息
    def get_trip_order(self,value):
        pass
















    def _close(self):
        try:
            self.conn.close()
        except Exception:
            raise NotImplementedError



if __name__ == '__main__':
    db=DB_Connection()
    res=db.get_city("北京")
    print(res)










































