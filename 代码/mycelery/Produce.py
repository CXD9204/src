#!/usr/bin/env/python
# coding=UTF-8
'''
@file          :   Produce.py
@Author        :   程牧扬
@Time          :   2022/3/8 13:52
@Version       :   1.0
@Describetion  :
'''
import logging
import json
from task import add
from task import send_mail
# group: 一组任务并行执行，返回一组返回值，并可以按顺序检索返回值。
# chain: 任务一个一个执行，一个执行完将执行return结果传递给下一个任务函数.
from celery import group, chain, signature
from task import task1, task3, task2, task4
from CeleryUtil import app


def mysignature(s)->"celery signature":
    s.delay()


if __name__ == '__main__':
    # 回调任务，父任务的结果将会作为参数传递给链接或chord的回调任务,apply_async 的 link 参数来添加回调。
    res = add.apply_async((1, 2), link=task1.s(4))
    print("回调:", res.get(propagate=False))
    print(add.delay(23, 15).get())
    # 签名，将任务变成一个可传递的参数,参数:countdown表示在10s内执行该任务
    signa = send_mail.signature((2, 2), countdown=10)
    signa = signature(send_mail, args=(2, 2))
    # 执行任务，或者将任务作为另一个函数的参数
    # signa.delay()
    mysignature(signa)
    # group并行执行
    myGroup = group(task1.s(1, 1), task2.s(2, 2), task3.s(3, 3), task4.s(4, 4))
    ret = myGroup()  # 执行组任务
    print("并发同步执行", ret.get())
    # chain并发执行
    myChain = chain(task1.s(1, 1) | task2.s(2) | task3.s(3) | task4.s(4))
    ret2 = myChain()  # 执行任务链
    print("同步执行", ret2.get())
    # 打印celery配置信息,table() 方法将返回结果转换为字典
    info = app.conf.table(with_defaults=False, censored=True)
    print("配置信息:\n")
    for k, v in info.items():
        print(f"{k}:{v}")
    # with_defaults 参数进行包含默认的配置信息,将配置作为调试信息或类似信息打印出来，过滤掉敏感信息,Celery 提供了集中打印配置信息工具，其中一个为 humanize()：
    info2 = app.conf.humanize(with_defaults=False, censored=True)
    print("humanize():\n", info2)
