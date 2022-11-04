#!/usr/bin/env/python
# coding=UTF-8
'''
@file          :   prometheus_cib.py
@Author        :   程牧扬
@Time          :   2022/11/2 8:57
@Version       :   1.0
@Describetion  :https://blog.csdn.net/u014305062/article/details/98636139
'''
import requests

URL = 'http://60.60.60.191:9090'


def prometheusQueryApi(url, API):
    '''
    :param url: 普罗米修斯地址
    :param API: 访问的接口API
    :return:
    '''
    return url + API


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


def prometheus_metric(url):
    API = "/metrics"
    response = requests.get(url=url + API)
    print(response.text)


def prometheus_series(prometheus_rul, expr):
    '''
    通过标签匹配器查找系列
    :return:
    '''
    API = '/api/v1/series?' + expr
    response = requests.get(url=prometheus_rul + API)
    print(response.text)


def prometheus_query(prometheus_url, expr):
    '''
    :param prometheus_url: 普罗米修斯
    :param expr:普罗米修斯表达式
    :return:
    '''
    API = "/api/v1/query?query=" + expr
    response = requests.get(url=prometheus_url + API)
    result = response.text
    print(result)


# 查询指标元数据,
def prometheus_query_metadata(prometheus_url, metric, limit=None):
    '''
    :param prometheus_url: 地址
    :param metric: 查询指标
    :param limit: 显示行数
    :return:
    '''
    API = "/api/v1/metadata?limit=%s&metric=%s"(limit, metric)
    response = requests.get(url=prometheus_url + API)
    print(response.text)


if __name__ == '__main__':
    url = 'http://60.60.60.191:9090'
    # prometheus_metric(url)
    expr = "node_netstat_Tcp_RetransSegs{instance=“60.60.60.151:9101”，job=“151linux”}"
    # prometheus_query(url, expr)
    # 通过标签匹配器查找系列
    # curl -g 'http://localhost:9090/api/v1/series?'
    # --data-urlencode 'match[]=up'
    # --data-urlencode 'match[]=process_start_time_seconds{job="prometheus"}'
    expr2 = "--data-urlencode 'match[]=node_netstat_Tcp_RetransSegs' "
    # prometheus_series(url, expr2)
