#!/usr/bin/env python
# _*_ coding:utf-8_*-
'''
@Author:cheng
@file:.py
@Time:2022/11/6 11:13
@Describtion:
'''
import win32netcon
from prometheus_client import Enum, Counter, Summary, Histogram,Gauge
from prometheus_client import start_http_server, CollectorRegistry, push_to_gateway
import time
import random

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
# 枚举
e = Enum('my_task_state', 'Description of enum',
         states=['starting', 'running', 'stopped'])
# 计数器
c = Counter("my_failures", "Description od counter")


# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(t):
    """A dummy function that takes some time """
    time.sleep(t)


def PushToGateway():
    registry1 = CollectorRegistry()
    g = Gauge('job_last_success_unixtime', 'Last time a batch job successfully finished', registry=registry1)
    g.set_to_current_time()
    push_to_gateway("192.168.177.132:9091", job="151linux", registry=registry1)


if __name__ == '__main__':
    # start_http_server(9090,addr="60.60.60.191")
    while True:
        # process_request(random.random())
        PushToGateway()
