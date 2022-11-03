#!/usr/bin/env/python
# coding=UTF-8
'''
@file          :   gateway.py
@Author        :   程牧扬
@Time          :   2022/11/2 15:53
@Version       :   1.0
@Describetion  :desc: WSGI服务器实现
'''
from wsgiref.simple_server import make_server
from webservice import app


def main():
    sever = make_server('localhost', 8008, app)
    sever.serve_forever()


if __name__ == '__main__':
    main()
