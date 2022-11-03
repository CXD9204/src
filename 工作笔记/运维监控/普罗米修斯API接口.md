参考文档:[HTTP API |普罗 米修斯 (prometheus.io)](https://prometheus.io/docs/prometheus/latest/querying/api/)

HTTP API可以在Prometheus服务器上访问。任何不间断的添加都将添加到该终结点下/api/v1

即时查询

get  /api/v1/query

post /api/v1/query

参数:

query=<string>:普罗米修斯表达式查询字符串

time:评估时间戳

timeout: 超时时间

范围查询

```
GET /api/v1/query_range
POST /api/v1/query_range
网址查询参数：

query=<string>：普罗米修斯表达式查询字符串。
start=<rfc3339 | unix_timestamp>：开始时间戳（含）。
end=<rfc3339 | unix_timestamp>：结束时间戳（含）。
step=<duration | float>：格式或浮点数的查询解析步长宽度。duration
timeout=<duration>：评估超时。自选。默认为标志的值，并受其限制。-query.timeout
```

标签匹配器查找系列

以下终结点返回与特定标签集匹配的时序列表

```
GET /api/v1/series
POST /api/v1/series
网址查询参数：
match[]=<series_selector>：重复的序列选择器参数，用于选择要返回的序列。必须至少提供一个参数。match[]
start=<rfc3339 | unix_timestamp>：开始时间戳。
end=<rfc3339 | unix_timestamp>：结束时间戳。
```

获取标签名称

返回终结点的标签名称列表

```
GET /api/v1/labels
POST /api/v1/labels
```