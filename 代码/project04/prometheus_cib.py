#!/usr/bin/env/python
# coding=UTF-8
'''
@file          :   prometheus_cib.py
@Author        :   程牧扬
@Time          :   2022/11/2 8:57
@Version       :   1.0
@Describetion  :https://blog.csdn.net/u014305062/article/details/98636139
'''
import requests

URL = 'http://60.60.60.191:9090'
response = requests.get(url=URL + '/api/v1/targets')
try:
    url = []
    if response.status_code:
        print(response.json()['data']['activeTargets'][1])
        for discover in response.json()['data']['activeTargets']:
            url.append(discover['scrapeUrl'])
            text = response.text
    print(url)
    response1=requests.get(url=url[1])
    textList=response1.text.split("\n")
    print(len(textList))
    for text in textList :
        if text.startswith("#"):
            textList.remove(text)
    print(len(textList))
    for text in textList:
        print(text)

except Exception as e:
    print(123)
    print(e)
