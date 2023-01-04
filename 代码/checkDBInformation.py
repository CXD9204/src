#!/usr/bin/env/python
# coding=UTF-8
'''
@file          :   checkDBInformation.py
@Author        :   程牧扬
@Time          :   2022/9/8 14:50
@Version       :   1.0
@Describetion  :
'''


def get_mysql_exec_results(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def slowQuery(conn) -> "慢查询":
    sql = "show full processlist"
    return get_mysql_exec_results(conn, sql)


def exec_max_times_sql(conn) -> '执行次数最多的sql':
    sql = '''SELECT
DIGEST_TEXT,
COUNT_STAR,
FIRST_SEEN,
LAST_SEEN
FROM
performance_schema.events_statements_summary_by_digest
ORDER BY
COUNT_STAR DESC;'''

    return get_mysql_exec_results(conn, sql)


def test(conn):
    sql = "select * from teacher"
    curses = conn.cursor()
    curses.execute(sql)
    result = curses.fetchall()

    # print(result)
    return result


def check_binlog(conn) -> '二进制日志检查':
    pass


def response_max_spend_sec_sql(conn: "数据库连接驱动") -> '平均响应时间最大的sql':
    sql = '''SELECT
DIGEST_TEXT,
AVG_TIMER_WAIT,
COUNT_STAR,
FIRST_SEEN,
LAST_SEEN
FROM
performance_schema.events_statements_summary_by_digest
ORDER BY
AVG_TIMER_WAIT DESC;'''

    return get_mysql_exec_results(conn, sql)


def exec_max_order_rows_sql(conn) -> "排序记录最多的一次":
    sql = '''
    SELECT
DIGEST_TEXT,
SUM_SORT_ROWS,
COUNT_STAR,
FIRST_SEEN,
LAST_SEEN
FROM
performance_schema.events_statements_summary_by_digest
ORDER BY
SUM_SORT_ROWS DESC;
    '''
    return get_mysql_exec_results(conn, sql)


def scan_max_rows_sql(conn) -> "扫描最多的记录数":
    sql = '''SELECT	DIGEST_TEXT,	SUM_ROWS_EXAMINED,	COUNT_STAR,	FIRST_SEEN,	LAST_SEEN FROM	`performance_schema`.events_statements_summary_by_digest ORDER BY	SUM_ROWS_EXAMINED DESC;'''
    return get_mysql_exec_results(conn, sql)


def create_max_tmp_tables_sql(conn) -> "创建临时表最多的sql":
    sql = '''SELECT DIGEST_TEXT,SUM_CREATED_TMP_TABLES,	SUM_CREATED_TMP_DISK_TABLES,COUNT_STAR,	FIRST_SEEN,	LAST_SEEN FROM	`performance_schema`.events_statements_summary_by_digest ORDER BY SUM_CREATED_TMP_TABLES DESC,SUM_CREATED_TMP_DISK_TABLES DESC'''
    return get_mysql_exec_results(conn, sql)


def get_max_result_sql(conn) -> "返回结果集最多的sql语句":
    sql = '''SELECT DIGEST_TEXT, SUM_ROWS_SENT, COUNT_STAR, FIRST_SEEN, LAST_SEEN  FROM `performance_schema`.events_statements_summary_by_digest ORDER BY SUM_ROWS_SENT DESC;'''
    return get_mysql_exec_results(conn, sql)


def max_physical_IO_sql(conn) -> "表物理IO最多的":
    sql = '''SELECT 	file_name, event_name, SUM_NUMBER_OF_BYTES_READ, SUM_NUMBER_OF_BYTES_WRITE  FROM `performance_schema`.file_summary_by_instance  ORDER BY SUM_NUMBER_OF_BYTES_READ + SUM_NUMBER_OF_BYTES_WRITE DESC;'''
    return get_mysql_exec_results(conn, sql)


def max_logical_read_sql(conn) -> '表逻辑读最多':
    sql = '''SELECT object_schema, 	object_name, COUNT_READ, COUNT_WRITE, COUNT_FETCH, SUM_TIMER_WAIT  FROM `performance_schema`.table_io_waits_summary_by_table  ORDER BY 	sum_timer_wait DESC;'''
    return get_mysql_exec_results(conn, sql)


def wait_event_max_time(conn) -> "消耗时间最多的等待事件":
    sql = '''SELECT EVENT_NAME, COUNT_STAR, SUM_TIMER_WAIT, AVG_TIMER_WAIT  FROM `performance_schema`.events_waits_summary_global_by_event_name  WHERE 	event_name != 'idle'  ORDER BY 	SUM_TIMER_WAIT DESC;'''
    return get_mysql_exec_results(conn, sql)
