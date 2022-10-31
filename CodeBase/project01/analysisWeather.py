import pymysql

HOST = "localhost"
PORT = 3306
USER = 'root'
PASSWORD = "123456"
DATABASE = 'one'


class DBUTIL(object):
    def __init__(self, ip, port, user, password, database):
        self.ip = ip
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.conn = pymysql.connect(host=self.ip, port=self.port, user=self.user, password=self.password,
                                    database=self.database, charset='utf8')
        self.cursor = self.conn.cursor()

    def exec_sql(self, sql):
        row = self.cursor.execute(sql).fetchall()
        return row

    def setClose(self):
        self.conn.close()


def createObj(ip, port, user, password, database):
    if ip and port and user and password and database:
        return DBUTIL(ip, port, user, password, database)
    else:
        print("参数不为空")
        return None


sql='''
create or replace table weather(

)

'''
