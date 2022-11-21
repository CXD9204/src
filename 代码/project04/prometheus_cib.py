#!/usr/bin/env/python
# coding=UTF-8
'''
@file          :   prometheus_cib.py
@Author        :   程牧扬
@Time          :   2022/11/2 8:57
@Version       :   1.0
@Describetion  :https://blog.csdn.net/u014305062/article/details/98636139
'''
import json
from pandas import DataFrame
import requests

URL = 'http://60.60.60.191:9090'


def prometheusQueryApi(url, API):
    '''
    :param url: 普罗米修斯地址
    :param API: 访问的接口API
    :return:
    '''
    return url + API


# 查找服务主机
def target_url():
    response = requests.get(url=URL + '/api/v1/targets')
    try:
        url = []
        if response.status_code:
            print(response.json()['data']['activeTargets'][1])
            for discover in response.json()['data']['activeTargets']:
                url.append(discover['scrapeUrl'])
                text = response.text
    except Exception as e:
        print(123)
        print(e)


# 查询普罗米修斯的指标列表
def prometheus_metric(url):
    '''
    http://60.60.60.191:9090/metrics?{instance= "60.60.60.151:9101",job='151linux'} 指定实列的指标
    :param url:
    :return:
    '''
    API = "/metrics"
    response = requests.get(url=url + API)
    print(response.text)


# 通过标签匹配器查找系列指标
def prometheus_series(prometheus_url):
    '''
    http://60.60.60.191:9090/api/v1/series?match[]={instance="60.60.60.191",job="Linux主机"}
    :return:
    '''
    expr = '{instance= "60.60.60.151:9101",job="151linux"}'
    # API = '/api/v1/series?' + " " + expr
    API = '/api/v1/series?match[]={instance="60.60.60.191:9090"}'
    PrometheusUrlApi = prometheusQueryApi(prometheus_url, API)
    print(PrometheusUrlApi)
    response = requests.get(url=PrometheusUrlApi)
    print(response.json())
    for data in response.json():
        print(data)


# 普罗米修斯 查询
def prometheus_query(prometheus_url, expr):
    '''
    :param prometheus_url: 普罗米修斯
    :param expr:普罗米修斯表达式
    :return:
    '''
    metric = 'node_memory_MemTotal_bytes'
    API = "/api/v1/query?query=" + expr
    PrometheusUrlApi = prometheusQueryApi(prometheus_url, API)
    response = requests.get(url=PrometheusUrlApi)
    result = response.json()
    print(result)
    if result['status'] == 'success':
        dataset = result['data']['result']
        metric_value = dataset[0]['value']
        total_value = sum(float(value) for value in metric_value)
        # 格式转化 将byte转接为MB
        print(total_value / len(metric_value) / 1024 / 1024)


def queryAllPrometheusMetricValue(prometheus_url, expr):
    '''
    一次性获取所有普罗米修斯指标
    :return:
    http://60.60.60.191:9090/api/v1/query?query={instance= "60.60.60.151:9101",job='151linux'}
    '''
    expr = '{instance= "60.60.60.151:9101",job="151linux"} '
    API = "/api/v1/query?query=" + expr
    response = requests.get(url=prometheusQueryApi(prometheus_url, API))
    if response.json()['status'] == 'success':
        resultDict = response.json()['data']['result']
        return resultDict
    elif response.json()['status'] == 'error':
        print("请求失败查询错误")
    else:
        return None


# 查询指标元数据,
def prometheus_query_metadata(prometheus_url, metric, limit=None):
    '''
    :param prometheus_url: 地址
    :param metric: 查询指标
    :param limit: 显示行数
    :return:
    '''
    API = "/api/v1/metadata?limit=%s&metric=%s" % (limit, metric)
    response = requests.get(url=prometheus_url + API)
    print(response.text)


if __name__ == '__main__':
    PATH = "F:\DFC\I6000健康管理\配电网工程标准化设计管理系统\\21.47.38.204.txt"
    dataDict = dict()
    with open(PATH, 'r+', encoding="utf-8") as f:
        result = f.readlines()
        dataDict = json.loads(result[0])['data']
    dataList = dataDict['result']
    metricList=[]
    valueList=[]
    for data in dataList:
        metricList.append(data['metric'])
        valueList.append(data['value'][1])

    df=DataFrame(metricList)
    df['value']=valueList
    df.to_excel('metric.xlsx',index=False,index_label=False)

