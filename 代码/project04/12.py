#!/usr/bin/env/python
# coding=UTF-8
'''
@file          :   12.py
@Author        :   程牧扬
@Time          :   2022/11/10 17:22
@Version       :   1.0
@Describetion  :
'''
import requests


# from baidu_trans import BaiDu

def AcquireProMetricApi(url, expr):
    return url + expr


def AcquirePrometheusJsonData(resp):
    if resp.json()['status'] == "success" and resp.json()['data']:
        return resp.json()['data']
    elif resp.json()['status'] == "success" and resp.json()['data'] is None:
        print("查询不存在")
        return None
    else:
        print("查询失败")


# 指标元信息
def QueryPrometheusMetricInfo(url, expr, metricList):
    expr1 = "/api/v1/metadata?limit=5&metric="
    jsonList = []
    for metric in metricList:
        dataDict = {}
        expr = expr1 + metric
        response = requests.get(url=AcquireProMetricApi(url, expr))
        jsonData = AcquirePrometheusJsonData(response)
        if jsonData is None:
            continue
        for key, value in jsonData.items():
            dataDict['metric'] = key
            dataDict['metric_desc'] = value[0]['help']
            jsonList.append(dataDict)
    return jsonList


def QueryPrometheusMetric(url, expr):
    response = requests.get(url=AcquireProMetricApi(url, expr))
    jsonData = AcquirePrometheusJsonData(response)
    resultList = jsonData['result']
    jsonList = []
    for result in resultList:
        metric_name = result['metric']['__name__']
        jsonList.append(metric_name)
    return jsonList


def toCSV(JsonList):
    from pandas import DataFrame
    df = DataFrame(jsonList)
    df = df.drop_duplicates(['metric', 'metric_desc'], keep='first')
    df.to_csv('meiric.csv', index_label=False)


if __name__ == '__main__':
    url = "http://60.60.60.191:9090"
    expr = '/api/v1/query?query={instance="60.60.60.191",job="Linux主机"}'
    result = QueryPrometheusMetric(url, expr)
    jsonList = QueryPrometheusMetricInfo(url, expr=None, metricList=result)
    for json in jsonList:
        print(json)
    toCSV(jsonList)
