#!/usr/bin/env/python
# coding=UTF-8

broker_url = 'redis://localhost:6369/1'
result_backend = 'redis://localhost:6379/0'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
task_result_expires = 60 * 60 * 24  # celery任务结果有效期
timezone = 'Asia/Shanghai'
enable_utc = True
