#!/usr/bin/env/python
# coding=UTF-8
'''
@file          :   webservice.py
@Author        :   程牧扬
@Time          :   2022/11/2 15:57
@Version       :   1.0
@Describetion  :
'''
from flask import Flask

app = Flask(__name__)


@app.route("/hello", methods=["GET", "POST"])
def get():
    return "hello,world"
