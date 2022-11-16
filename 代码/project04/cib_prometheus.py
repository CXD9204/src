#!/usr/bin/env/python
# coding=UTF-8
import sys
import traceback
import requests
import json
from datetime import datetime

URL = 'http://60.60.60.191:9090'


def cs(val, dt=False):
    if val is None:
        return ''
    else:
        if dt:
            return val.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(val)


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
    print(dataset)


def cib_ora_prometheus(url, metric):
    expr = '{instance= "60.60.60.151:9101",job="151linux"} '
    response = requests.get(url=PrometheusQueryApi(url, expr))


# 接口请求体数据
def cmdb_param(*args):
    '''
    :param args: 请求对象参数,
    :return:
    '''
    data = {
        "data": {
            "appSysCode": "test",
            f"{args[0]}": f"{args[1]}",
            "dataSource": "prometheus",
            "startDateTime": "2021-10-22 06:00:30",
            "endDateTime": "2021-10-22 06:00:35"
        }
    }
    return data


# cmdb接口访问响应结果处理
def ResponseData(response):
    '''
    :param response: request请求响应对象
    :return:
    '''
    resultList = None
    isuccess = response.json['success']
    if isuccess:
        dataDict = response.json['data']['data']
        resultList = dataDict['result']
    return resultList


def cib_cmdb_by_metric(metric_name):
    '''
    :return: 指标,指标值
    '''
    cmdb_url = "http://monitor.center.js.sgcc.com.cn:18000/monitor-center/api/metric/query"
    data = {
        "data": {
            "appSysCode": "test",
            "code": f"{metric_name}",
            "dataSource": "prometheus"
        }
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        "Content-Type": "application/json"
    }

    response = requests.post(url=cmdb_url, headers=headers, data=data, timeout=35)

    resultList = ResponseData(response)
    for result in resultList:
        metric_check(result,)


# cmdb指标采集整理
def metric_check(metricList, targetMetric, metric, *args):
    '''
    :param metricList: 指标列表
    :param targetMetric: 普罗米修斯指标
    :return:
    '''
    value = 0.0
    dataDict = dict()
    if metricList['__name__'] == targetMetric:
        value = sum(float(value) for value in metricList['values'][1]) / len(metricList['values']) * 1.0
        dataDict['index_id'] = args[0]
        dataDict[' cib_bame'] = args[1]
        dataDict[' cib_value'] = cs(value)
    metric.append(dataDict)


# cmdb指标采集匹配
def cib_cmdb_all_metric(url, metric, *target):
    response = requests.post(url=url, data=cmdb_param(*target), timeout=35)
    resultList = ResponseData(response)
    for result in resultList:
        metric_check(result, 'node_memory_MemTotal_bytes', metric, ['80150513', "MemSize".lower()])  # 内存大小
        metric_check(result, 'node_memory_MemAvailable_bytes', metric, ['80150521', "MemAvailable".lower()])  # 可用内存大小
        metric_check(result, 'node_memory_MemFree_bytes', metric, ['80150522', "MemFree".lower()])  # 剩余内存大小
        metric_check(result, 'node_disk_written_bytes_total', metric,['801505010', "FileSystemUsedRatio".lower()])  # 磁盘写入字节数
        metric_check(result, 'node_network_carrier', metric, ['80150509', "NetTotalRate".lower()])  # 网络负载
        metric_check(result, 'node_procs_blocked', metric, ['80150523', "ProcsBlocked".lower()])  # 当前被阻塞的任务的数目
        metric_check(result, 'node_procs_running ', metric, ['80150524', "ProcsRunning".lower()])  # 当前运行队列的任务的数目
        metric_check(result, 'node_memory_SwapTotal_bytes', metric, ['80150525', "SwapSize".lower()])  # Swap交换区大小
        metric_check(result, 'node_memory_SwapFree_bytes', metric, ['80150526', "SwapFree".lower()])  # Swap剩余交换区大小
        metric_check(result, 'node_load1', metric, ['80150527', "CpuLoadAverage1m".lower()]) #cpu1分钟负载
        metric_check(result, 'node_load5', metric, ['80150528', "CpuLoadAverage5m".lower()]) #cpu1分钟负载
        metric_check(result, 'node_load15', metric, ['80150529', "CpuLoadAverage15m".lower()]) #cpu1分钟负载

        metric_check(result, 'node_memory_MemFree_bytes', metric, ['80150522', "MemFree".lower()])
        metric_check(result, 'node_memory_MemFree_bytes', metric, ['80150522', "MemFree".lower()])
        metric_check(result, 'node_memory_MemFree_bytes', metric, ['80150522', "MemFree".lower()])


def cib_os_prometheus(url, metric):
    node_memory_MemAvailable_bytes = None
    node_memory_MemTotal_bytes = None
    node_memory_MemFree_bytes = None
    expr = '/api/v1/query?query={instance= "60.60.60.151:9101",job="151linux"}'
    response = requests.get(url=PrometheusQueryApi(url, expr), timeout=30)
    dataDict = DealPrometheusData(response, metric)
    reslultList = dataDict['result']
    for result in reslultList:
        print(result)
        # 内存指标信息
        if result['metric']['__name__'] == "node_memory_MemFree_bytes":
            node_memory_MemFree_bytes = result['value'][1]
            metric.append(dict(index_id='2210001', cib_bame=result['metric']['__name__'].lower(),
                               cib_value=cs(node_memory_MemFree_bytes)))

        if result['metric']['__name__'] == "node_memory_MemTotal_bytes":
            node_memory_MemTotal_bytes = result['value'][1]

        if result['metric']['__name__'] == "node_memory_MemAvailable_bytes":
            node_memory_MemAvailable_bytes = result['value'][1]

    print(node_memory_MemTotal_bytes, node_memory_MemAvailable_bytes, node_memory_MemFree_bytes)


if __name__ == '__main__':
    try:
        metric = []
        return_dict = dict()
        dbinfo = eval(sys.argv[1])
        target_ip = dbinfo['target_ip']
        target_port = dbinfo['target_port']
        target_url = dbinfo['target_url']
        # 数据采集
        cib_cmdb_all_metric(target_url, metric, [target_ip, target_port])

        # 数据处理放返回格式
        return_dict['cibInfos'] = metric
        cur_time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        return_dict["collectionTime"] = cur_time
        return_dict["dataTime"] = cur_time
        return_dict["hasError"] = False
        return_dict["errorMsg"] = ""
        print('[' + json.dumps(return_dict, ensure_ascii=False) + ']')
    except Exception as e:
        print(e)
        # return_dict["errorMsg"] = traceback.format_exc()
        # return_dict["hasError"] = True
        # return_dict["indexType"] = "221"
        # print('[' + json.dumps(return_dict, ensure_ascii=False) + ']')
