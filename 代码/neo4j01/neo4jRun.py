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
index_ids = [{'indexId': '80020007', 'value': '49.59', 'symbol': '>'}]

cql = "match(n:指标) where n.指标ID=80020007 return n.object_type as object_type,n.指标名称 as metric_name"
with app.driver.session() as session:
    result = session.run(cql)
    print(result.data())
print(app.analysis_metric(index_ids))

cql1 = "match (n:运维经验) where n.object_type='%s' and n.`指标项`='%s' return n" % ("oracle", "OracleInstMemorySortLoad")
with app.driver.session() as session:
    dataset = session.run(cql1).data()
    print(result)
