#!/usr/bin/env/python
# coding=UTF-8
'''
@file          :   one_celery.py
@Author        :   程牧扬
@Time          :   2022/3/3 12:41
@Version       :   1.0
@Describetion  :
'''
from celery import Celery
from os import path
import sys
import os

sys.path.append(path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mycelery

app = Celery(main=None, broker='redis://192.168.177.132:6379/0', backend='redis://192.168.177.132:6379/1')

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='Europe/Oslo',
    enable_utc=True
)
# app.config_from_object(mycelery.CeleryUtil)
# app.conf.timezone = 'UTC'
# 调度器


# 通过 app.config_from_object() 进行加载配置模块
# app.config_from_object("celeryconfig")

if __name__ == '__main__':
    app = Celery("main")
    for data in app.conf:
        if data is None:
            continue
        print(data)
    print(app.conf)
