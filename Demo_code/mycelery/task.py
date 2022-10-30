#!/usr/bin/env/python
# coding=UTF-8
'''
@file          :   task.py
@Author        :   程牧扬
@Time          :   2022/3/4 11:01
@Version       :   1.0
@Describetion  :
'''

from CeleryUtil import app


# app.Task.request 包含与当前执行任务相关的信息和状态,
@app.task(name="mytask1", bind=True)
def task1(self, x, y) -> "测试x+y之和,并返回值":
    print("任务1执行中………………")
    print(
        'Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r} origin:{0.origin!r} hostname:{0.hostname!r}'.format(
            self.request))
    return x + y


@app.task
def task2(x, y):
    print("任务2执行中………………")
    return x + y


@app.task
def task3(x, y):
    print("任务3执行中………………")
    return x + y


# 每一个任务都必须有一个唯一任务名称。 如果没有指定任务名称，装饰器会根据当前任务所在的模块以及任务函数的名称进行生成一个
@app.task(name="mytask4")
def task4(x, y):
    print("任务4执行中………………")
    return x + y


@app.task
def add(x, y):
    print("任务5执行中………………")
    return x + y


@app.task
def send_mail(x, y):
    '''
    :param From: 发送人
    :param To: 接收人
    :param mail: 邮件内容
    :return:
    '''

    print("任务执行中………………")
    return x - y

# if __name__ == '__main__':
# result = add.delay(4, 5)
# print(result.backend)
# 查看任务是否处理完毕
# print(result.ready())
# 查看任务执行结果
# print(result.get(propagate=False))  # 不希望celery 抛出异常
# 获取任务ID
# print(result.id)
# 检测任务失败还是成功：
# result.failed()  # 任务是否失败
# result.successful()  # 任务是否失败
