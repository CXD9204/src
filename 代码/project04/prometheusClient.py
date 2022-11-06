#!/usr/bin/env python
# _*_ coding:utf-8_*-
'''
@Author:cheng
@file:.py
@Time:2022/11/6 11:13
@Describtion:
'''
import win32netcon
from prometheus_client import Enum, Counter, Summary, Histogram
from prometheus_client import start_http_server
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


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)


    while True:
        process_request(random.random())
        e.state('running')
        # e.state("stopped")
        e.state('running')
        c.inc()
