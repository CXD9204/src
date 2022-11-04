#!/usr/bin/env/python
# coding=UTF-8
'''
@file          :   savemetricvalue.py
@Author        :   程牧扬
@Time          :   2022/11/4 14:38
@Version       :   1.0
@Describetion  :
'''
import pymysql
import prometheus_cib

HOST = "localhost"
PORT = 3306
USER = 'root'
PASSWORD = '123456'
DATABASE = 'demo'


class MYSQL():
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                    database=self.database)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def __repr__(self):
        print("mysql connect is %s" % (self.conn))


def prometheus():
    url = 'http://60.60.60.191:9090'
    expr = '{instance= "60.60.60.151:9101",job="151linux"} '
    API = "/api/v1/query?query=" + expr
    result = prometheus_cib.queryAllPrometheusMetricValue(url, expr)
    return result


if __name__ == '__main__':
    sql = '''
   drop table if exists prometheus;
    create  table prometheus(
    name varchar(10),
    device varchar(10),
    instance varchar(10),
    job varchar(5),
    value varchar(10)
        )'''
    mysql = MYSQL(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE)
    # cursor.execute(sql)
    cursor = mysql.cursor
    for metric in prometheus():
        name = metric['metric']["__name__"]
        instance = metric['metric']["instance"]
        job = metric['metric']["job"]
        value1 = (sum(float(value)) / len(metric['value']) for value in metric['value'])
        value=str(metric['value'][1])
        sql = f'insert into prometheus(name,instance,job,value)values("{name}","{instance}","{job}","{value}")'
        cursor.execute(sql)
        mysql.conn.commit()
        print(name,instance,job,value)
