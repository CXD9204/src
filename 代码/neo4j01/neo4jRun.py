#!/usr/bin/env/python
# coding=UTF-8
'''
@file          :   neo4jRun.py
@Author        :   程牧扬
@Time          :   2022/11/1 14:52
@Version       :   1.0
@Describetion  :
'''
from Neo4jUtil import App

USER = "neo4j"
PASSWORD = "DCF@Neo4j3"
URL = "neo4j://60.60.60.16:7687"
app = App(URL, USER, PASSWORD)
conclusion = []
index_ids = {
    'indexId': '80020007',
    'symbol': ''
}
print(app.acquire_solution(conclusion,index_ids))
