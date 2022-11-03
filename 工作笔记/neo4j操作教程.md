W3C学习网站:https://www.w3cschool.cn/neo4j/neo4j_cql_create_label.html

密码参考：https://neo4j.com/docs/cypher-refcard/current/

安装：

下载neo4j安装包

配置 neo4j的环境变量

NEO4J_HOME=D:\neo4j-community-3.5.5

path追加环境变量

path=%NEO4J_HOME%\bin

启动：

方式1、neo4j.bat console

把Neo4J安装作为服务

neo4j install-service 

neo4j uninstall-service

Neo4j构建4元素：

节点

属性

关系

标签

### CQL关键字

| CQL命令  | 用法                                                         |                                                             |
| -------- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| create   | 创建节点 关系和属性                                          |                                                             |
| match    | 检索有关节点 关系和属性数据                                  |                                                             |
| return   | 返回查询结果                                                 |                                                             |
| where    | 提供过滤条件和过滤检索数据                                   | start with:以……开头   ；ends with:以……结束；  contains:包含 |
| delete   | 删除节点和关系                                               | 删除节点必须先删除关系                                      |
| DETACH   | 删除某个节点的同时也删除关系                                 |                                                             |
| remove   | 删除节点和关系属性                                           |                                                             |
| order by | 排序检索数据                                                 |                                                             |
| set      | 添加和更新属性标签                                           | 类似SQL中的update                                           |
| unwind   | 将任何列表转换回单独的行                                     |                                                             |
| with     | `WITH`子句允许将查询部分链接在一起，将一个结果作为下一个起点或标准进行管道传输 |                                                             |

### CQL操作

查询节点：MATCH (n:Persion) where n.name='孙悟空'RETURN n LIMIT 25

#### 查询节点并添加关系：

match (n:Persion {name:'猪八戒'}),(m:Persion {name:'孙悟空'}) create (n)-[r:同门] ->(m)return n,m 

#### 子查询_in：

match (n:Persion)where n.name in ["孙悟空","唐僧"] return n

#### unwind 操作：

with [1,23,4,5] as a,[3,4,5,6,7] as b unwind (a+b) as x return x

链接多个子句以展开嵌套列表元素：

WITH [[1, 2], [3, 4], 5] AS nested UNWIND nested AS x UNWIND x AS y RETURN y

#### 子查询_with

| 操作                             | CQL                                                          |
| -------------------------------- | ------------------------------------------------------------ |
|                                  | MATCH (n:`指标属性`)-[:属于]-(m:`指标`) with m return m      |
| 通配符* 传递变量                 | MATCH (n:`统计信息`)-[r]->(m:`指标`) with *, type(r) as friend return n.ip,m.index_desc,friend |
| 将重复的列表转换为集合`DISTINCT` | match(n:`指标`) with * ,n.object_type as coll unwind coll as x WITH DISTINCT x<br/>RETURN collect(x) AS setOfVals |
|                                  |                                                              |

#### 过滤聚合函数结果

#### 创建索引：

create index on 

#### 导入csv文件：

load csv from "file:///IT.csv" as line

create(oracle:Oracle{index_id:line[1],object_type:line[2],index_name:line[3],index_desc:line[4],unit:line[5],data_from:line[6], data_from_id:line[7],index_mark:line[8]}) return oracle

#### 读取文件

load csv with headers from "file:///pg_index_catalog.csv" as line with *,line.param2 as x where x is not null return line

#### 直接检索节点关系：

MATCH p = (:DB {name:'oracle'})-[:指标]-(:`指标编码`)

RETURN p

#### 相关节点

--表示相关，不考虑类型和方向

match(n:DB{name:'oracle'})--(m:`指标编码`) return m,n

#### 标签改名：

先删除旧的指标名称 在添加新的指标名称

MATCH (n:`指标编码`) remove n:`指标编码` set n:`诊断指标` return n

#### 修改属性名称

```
match(n:CAR) ``SET` `n.new_property ``=` `n.old_property remove n.old_proerty
```

#### case语句

MATCH (n:`DS_运维经验`) with n,

case n.db_type

when "2101" then "oracle"

when "2102" then "mysql"

when "2103" then "dm"

when "2104" then "postgres/金仓/瀚高"

when "2105" then   "sqlserver"

when "2106"  then "GS100"

when "2108"  then "redis"

when "2109"  then   "mongodb"

when "2903"  then  "kafka"

when "2901"  then  "Patroni"

when "2501"  then  "tomcat"

when "2502"  then "weblogic"

when "2602"  then  "华为存储"
end as type_db
set n.type_name=type_db  //新增DS_运维经验中type_type属性 

//

//删除DS_运维经验中db_type属性  新增type_id属性  且n.type_id=n.db_type

match (n:DS_运维经验) set n.type_id=n.db_type remove n.db_type

#### 删除标签属性值

MATCH p=()-[r:`属于`]->() delete r

################################################

录入异常分析数据：load csv from "file:///os_exception.csv" as line create (n:异常{classification:line[0],objects:line[1],I6_object:line[2],I6_indicator:line[3],I6_desc:line[4],reference_value:line[5],fault_name:line[6],fault_desc:line[7],solutions:line[8],IsLogFind:line[9],log_Character:line[10]}) return n

录入IT指标：load csv from "file:///IT.csv" as line

create(oracle:Oracle{index_id:line[1],object_type:line[2],index_name:line[3],index_desc:line[4],unit:line[5],data_from:line[6], data_from_id:line[7],index_mark:line[8]}) return oracle

OS指标类型关联：

create (n:类型{type_name:'OS'})

match(n:`类型`),(m:`异常`) create (m)-[:属于]->(n) return n

### neo4j函数

| 函数      | 描述             |      |
| --------- | ---------------- | ---- |
| size      | 获取属性长度     |      |
| toUpper   | 属性值大写       |      |
| toLower   | 属性值小写       |      |
| toInteger | 字符串转数据类型 |      |
| date      | 日期函数         |      |
| localtime | 当前本地时间     |      |
|           |                  |      |

size:获取属性值长度

### 注意事项

#### 数据库选择

只有当驱动程序连接到 Neo4j Enterprise Edition 时，才能选择数据库更改为 Neo4j 社区版中默认数据库以外的任何其他数据库将导致运行时错误

#### 会话创建时的数据库选择

with driver.session(database="example") as session

with driver.session(database="example", default_access_mode=READ_ACCESS) as session  访问模式:读事务

#### 配置连接池

def __init__(self, uri, auth):    

self.driver = GraphDatabase.driver(uri, auth=auth,                                       

max_connection_lifetime=30 * 60,     驱动程序将保持连接的最大持续时间 默认3600s                                  

max_connection_pool_size=50,            允许的最大连接总数 默认值100                           

connection_acquisition_timeout=2 * 60)

#### 数据备份

neo4j3种备份方式:

1、java在线备份（社区版本不支持）

2、neo4j-admin工具，需要在数据库关闭情况下本地备份

3、neo4j-backup工具，可在neo4j启动状态下在线备份，可远程备份

在采取备份前，需要在配置文件中增加以下内容:

dbms.backup.enabled=true

dbms.backup.address=<主机名或者ip>:6362

##### neo4j-admin备份：

*表示将graph.db数据库备份到/home/neo4j/databackup目录下，文件名称为：20190222.dump*

neo4j-admin dump --database=graph.db   --to=/home/neo4j/databackup/20190222.dump

##### neo4j-admin远程增量备份：

*fallback-to-full=true表示当正能量备份发生错误时候，转换成全量备份*

neo4j-admin backup --from 192.168.0.10 --backup-dir=/home/neo4j/databackup/ --name=graph.db_zlbf --fallback-to-full=true  --check- consistency=true

#### 数据恢复

使用neo4j-admin进行数据恢复，恢复之前需要关闭数据库

##### dump文件恢复:

neo4j-admin load --from=/home/neo4j/databackup/ 20190222.dump --database=graph.db --force

##### 备份数据恢复:

neo4j-admin restore --from=/home/neo4j/databackup/graph.db_backup --database=graph.db  --force

