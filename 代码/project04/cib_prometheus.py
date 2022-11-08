#!/usr/bin/env/python
# coding=UTF-8
import traceback
import requests
import json
import datetime

URL = 'http://60.60.60.191:9090'


# 普罗米修斯接口API查询处理函数
def PrometheusQueryApi(prometheus_url, expr):
    '''
    :param prometheus_url: 普罗米修斯URL
    :param expr: 接口参数
    :return: 普罗米修斯的HTTP查询接口
    例如:prometheus_url=http://localhost:9090,expr='/query?query{instance= "60.60.60.151:9101",job="151linux"} '
    返回:http://localhost:9090/query?query={instance= "60.60.60.151:9101",job="151linux"}
    '''
    return prometheus_url + expr


# 普罗米修斯响应结果数据处理
def DealPrometheusData(response, metric):
    if response.json()['status'] == "success" and response.json()['data']:
        dataset = response.json()['data']
        return dataset
    elif response.json()['status'] == "success" and response.json()['data'] is None:
        print("普罗米修斯接口请求数据为空,请确认")
        return None
    else:
        print("普罗米修斯请求错误")
        return response.json()['error']


# 采集事例
def cib_os_demo(url, metric):
    expr = '{instance= "60.60.60.151:9101",job="151linux"}'
    response = requests.get(url=PrometheusQueryApi(url, expr), timeout=30)
    dataset = DealPrometheusData(response, metric)


def cib_ora_prometheus(url, metric):
    expr = '{instance= "60.60.60.151:9101",job="151linux"} '
    response = requests.get(url=PrometheusQueryApi(url, expr))


def cib_mysql_prometheus():
    pass


def cib_tomcat_prometheus():
    pass


def cib_wls_prometheus():
    pass


def cib_redis_prometheus():
    pass


def cib_pg_prometheus():
    pass


def cib_activeMQ_prometheus():
    pass


def cib_os_prometheus():
    pass


def cib_dm_prometheus():
    pass


def cib_mongodb_prometheus():
    pass


if __name__ == '__main__':
    try:
        metric = []
        return_dict = dict()
        # 数据采集
        cib_os_prometheus(URL, metric)

        # 数据处理放返回格式
        return_dict['cibInfos'] = metric
        cur_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        return_dict["collectionTime"] = cur_time
        return_dict["dataTime"] = cur_time
        return_dict["hasError"] = False
        return_dict["errorMsg"] = ""
        print('[' + json.dumps(return_dict, ensure_ascii=False) + ']')
    except Exception as e:
        return_dict["errorMsg"] = traceback.format_exc()
        return_dict["hasError"] = True
        return_dict["indexType"] = "221"
        print('[' + json.dumps(return_dict, ensure_ascii=False) + ']')
