#!/usr/bin/env/python
# coding=UTF-8
'''
@Describetion  :数据公共模块
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
    result = prometheus_cib.queryAllPrometheusMetricValue(url, expr)
    return result


if __name__ == '__main__':

    mysql = MYSQL(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE)
    cursor = mysql.cursor
    for metric in prometheus():
        name = metric['metric']["__name__"]
        instance = metric['metric']["instance"]
        job = metric['metric']["job"]
        value1 = metric['value']
        print(value1)
        value = str(metric['value'][1])
        sql = f'insert into prometheus(name,instance,job,value)values("{name}","{instance}","{job}","{value}")'
        cursor.execute(sql)
        mysql.conn.commit()
