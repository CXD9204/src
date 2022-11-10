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
from wsgiref.util import setup_testing_defaults
from webservice import app


def middleware():
    pass


def application(environ, start_response):
    headers = [('Content-type', 'text/plain')]
    status = '200 OK'
    start_response(status, headers)
    print(environ.get('wsgi.multiprocess'))
    return ['HELLO,WORLD'.encode('utf-8')]


def main():
    httpd = make_server('localhost', 8008, application)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
