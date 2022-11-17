## mysql数据库性能参数

数据变量分为全局变量（global）和当前会话变量（session）

mysql全局变量：

| 变量                      |                      |                    |
| ------------------------- | -------------------- | ------------------ |
| tx_isolation              | 查看隔离级别         |                    |
| auto_increament_increment | 查看全局自增变量     |                    |
| auto_increament_offset    | 默认主键起始值       |                    |
| max_connections           | 最大连接数           |                    |
| max_user_connections      | 最大用户连接数       |                    |
| myisam_recover_options    | 自动修复表           | 易导致数据库不可用 |
| skip_networking           | 服务器仅允许本地连接 |                    |
| general_log               |                      |                    |
|                           |                      |                    |

查看数据库引擎异常：show engine innodb status

## 数据库引擎

Innodb：主要实现行锁

实现行锁，锁定某一条记录：select * from table_name where id=1 for update 

show status like 'Innodb_row_lock%'

关键状态变量：

Innodb_row_lock_current_waits：  当前处于等待状态的锁数

Innodb_row_lock_time_avg：平均等待时长

Innodb_row_lock_waits：等待次数

Innodb_row_lock_time：总的等待时长

优化建议：

所有数据通过索引来完成，避免无索引行锁升级为表锁

合理设计索引，减小锁的范围

尽可能较少检索条件，避免间隙锁

控制事务大小，减小锁定资源和时间长度

尽可能低级事务隔离级别

MyISAM：表锁

间隙锁：用范围条件而不是相等条件检索数据，并请求共享锁或排它锁，InnoDB会对符合条件的已有数据记录的索引项增加行锁；对于键值在条件范围内但不存在的记录，叫做‘间隙’，InnoDB对该记录加锁，称为间隙锁

## 服务器性能分析

### IO

随机IO：SAS单盘不超过300  IOPS

SSD随机IO：35000 IOPS

### Memory

### CPU

第一范式：数据库表中的每一列数据都是不可分割的基本数据，同一个列中不可有多个值

第二范式：首先满足第一范式，另外还需要包含俩部分：表中的主键；没有包含在主键中的列必须完全依赖于主键，而不是只依赖于主键的一部分

### innoDB引擎系统表

#### 分区

• PARTITIONS：表分区

• FILES：存储MySQL NDB 磁盘数据表的文件

#### 特权

• COLUMN_PRIVILEGES：MySQL 用户帐户所拥有的列特权

• SCHEMA_PRIVILEGES：MySQL 用户帐户所拥有的数据库特权

• TABLE_PRIVILEGES：MySQL 用户帐户所拥有的表特权

• USER_PRIVILEGES：MySQL 用户帐户所拥有的全局特权

#### 字符集支持

• CHARACTER_SETS：可用的字符集

• COLLATIONS：每个字符集的整理

• COLLATION_CHARACTER_SET_APPLICABILITY：适用于特定字符集的整理

#### 约束和索引

• KEY_COLUMN_USAGE：关键列的约束

• REFERENTIAL_CONSTRAINTS：外键

• STATISTICS：表索引

• TABLE_CONSTRAINTS：表的约束

#### 服务器设置和状态

• KEY_COLUMN_USAGE：约束

• GLOBAL_STATUS：所有MySQL 连接的状态值

• GLOBAL_VARIABLES：用于新的MySQL 连接的值

• PLUGINS：服务器插件

• PROCESSLIST：指示哪些线程正在运行

• SESSION_STATUS：当前MySQL 连接的状态值

• SESSION_VARIABLES：当前MySQL 连接的生效值

例程及相关信息

• EVENTS：预定事件

• ROUTINES：存储过程和功能

• TRIGGERS：数据库中的触发器

• PARAMETERS：存储过程和功能参数以及存储函数

#### 表信息

• COLUMNS：表和视图中的列

• ENGINES：存储引擎

• SCHEMATA：数据库

• TABLES：数据库中的表

• VIEWS：数据库中的视图

#### InnoDB

• INNODB_CMP 和INNODB_CMP_RESET：对压缩的InnoDB 表的相关操作的状态

• INNODB_CMPMEM 和INNODB_CMPMEM_RESET：InnoDB 缓冲池中压缩页面的状态

• INNODB_LOCKS：InnoDB 事务所请求和持有的每个锁

• INNODB_LOCK_WAITS：每个阻塞的InnoDB 事务的一个或多个行锁

• INNODB_TRX：当前正在InnoDB 内部执行的所有事务

• TABLESPACES：活动的表空间



## 使用SQL

Performance Schema数据库的介绍，主要用于收集数据库服务器性能参数：

①提供进程等待的详细信息，包括锁、互斥变量、文件信息；

②保存历史的事件汇总信息，为提供MySQL服务器性能做出详细的判断；

③对于新增和删除监控事件点

通过Performance-Schema得到DBA关心的数据，比如哪个SQL执行次数最多，哪个表访问最频繁，哪个锁最热等信息



| 类别                            | SQL                                                          |
| ------------------------------- | ------------------------------------------------------------ |
| SQL维度分析                     |                                                              |
| 执行次数最多的SQL               | SELECT<br/>	DIGEST_TEXT,<br/>	COUNT_STAR,<br/>	FIRST_SEEN,<br/>	LAST_SEEN <br/>FROM<br/>`performance_schema`.events_statements_summary_by_digest <br/>ORDER BY<br/>	COUNT_STAR DESC; |
| 平均响应时间最大的sql           | SELECT<br/>	DIGEST_TEXT,<br/>	AVG_TIMER_WAIT,<br/>	COUNT_STAR,<br/>	FIRST_SEEN,<br/>	LAST_SEEN <br/>FROM<br/>	`performance_schema`.events_statements_summary_by_digest <br/>ORDER BY<br/>	AVG_TIMER_WAIT DESC; |
| 排序记录数最多的sql （影响CPU） | SELECT<br/>	DIGEST_TEXT,<br/>	SUM_SORT_ROWS,<br/>	COUNT_STAR,<br/>	FIRST_SEEN,<br/>	LAST_SEEN <br/>FROM<br/>	`performance_schema`.events_statements_summary_by_digest <br/>ORDER BY<br/>	SUM_SORT_ROWS DESC; |
| 扫描记录数最多的sql             | SELECT<br/>	DIGEST_TEXT,<br/>	SUM_ROWS_EXAMINED,<br/>	COUNT_STAR,<br/>	FIRST_SEEN,<br/>	LAST_SEEN <br/>FROM<br/>	`performance_schema`.events_statements_summary_by_digest <br/>ORDER BY<br/>	SUM_ROWS_EXAMINED DESC; |
| 使用临时表最多的sql             | SELECT<br/>	DIGEST_TEXT,<br/>	SUM_CREATED_TMP_TABLES,<br/>	SUM_CREATED_TMP_DISK_TABLES,<br/>	COUNT_STAR,<br/>	FIRST_SEEN,<br/>	LAST_SEEN <br/>FROM<br/>	`performance_schema`.events_statements_summary_by_digest <br/>ORDER BY<br/>	SUM_CREATED_TMP_TABLES DESC,<br/>	SUM_CREATED_TMP_DISK_TABLES DESC |
| 返回结果集最多的SQL             | SELECT<br/>	DIGEST_TEXT,<br/>	SUM_ROWS_SENT,<br/>	COUNT_STAR,<br/>	FIRST_SEEN,<br/>	LAST_SEEN <br/>FROM<br/>	`performance_schema`.events_statements_summary_by_digest ORDER BY SUM_ROWS_SENT DESC; |
| 对象维度分析：                  |                                                              |
| 那个表物理IO最多                | SELECT<br/>	file_name,<br/>	event_name,<br/>	SUM_NUMBER_OF_BYTES_READ,<br/>	SUM_NUMBER_OF_BYTES_WRITE <br/>FROM<br/>	`performance_schema`.file_summary_by_instance <br/>ORDER BY<br/>	SUM_NUMBER_OF_BYTES_READ + SUM_NUMBER_OF_BYTES_WRITE DESC; |
| 哪个表逻辑IO最多                | SELECT<br/>	object_schema,<br/>	object_name,<br/>	COUNT_READ,<br/>	COUNT_WRITE,<br/>	COUNT_FETCH,<br/>	SUM_TIMER_WAIT <br/>FROM<br/>	`performance_schema`.table_io_waits_summary_by_table <br/>ORDER BY<br/>	sum_timer_wait DESC; |
| **哪个索引访问最多**            | SELECT<br/>	OBJECT_SCHEMA,<br/>	OBJECT_NAME,<br/>	INDEX_NAME,<br/>	COUNT_FETCH,<br/>	COUNT_INSERT,<br/>	COUNT_UPDATE,<br/>	COUNT_DELETE <br/>FROM<br/>	`performance_schema`.table_io_waits_summary_by_index_usage <br/>ORDER BY<br/>	SUM_TIMER_WAIT DESC; |
| **哪个索引从来没有使用过**      | SELECT<br/>	OBJECT_SCHEMA,<br/>	OBJECT_NAME,<br/>	INDEX_NAME <br/>FROM<br/>	`performance_schema`.table_io_waits_summary_by_index_usage <br/>WHERE<br/>	INDEX_NAME IS NOT NULL <br/>	AND COUNT_STAR = 0 <br/>	AND OBJECT_SCHEMA <> 'mysql' <br/>ORDER BY<br/>	OBJECT_SCHEMA,<br/>	OBJECT_NAME; |
| 等待事件维度分析                |                                                              |
| 哪个等待事件消耗的时间最多      | SELECT<br/>	EVENT_NAME,<br/>	COUNT_STAR,<br/>	SUM_TIMER_WAIT,<br/>	AVG_TIMER_WAIT <br/>FROM<br/>	`performance_schema`.events_waits_summary_global_by_event_name <br/>WHERE<br/>	event_name != 'idle' <br/>ORDER BY<br/>	SUM_TIMER_WAIT DESC; |
|                                 |                                                              |

实例表：记录各类事件涉及到的实例

cond_instances：条件表

file_instances：列出执行文件I/O检测室性能模式能看到的所有文件

mutex_instances：互斥锁 ，

rwlock_instances：读写锁，列出性能架构在服务器执行看到的所有读写锁实例，

性能历史表：

SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
  -> WHERE TABLE_SCHEMA = 'performance_schema'
  -> AND (TABLE_NAME LIKE '%history' OR TABLE_NAME LIKE '%history_long');

history表只保留每个线程的最近10个事件

history_long：记录每个线程最近的10000个事件

这俩个表数据采用的是先进先出且只读，表满了的话  旧数据会被丢弃

事件汇总表：

SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES
  -> WHERE TABLE_SCHEMA = 'performance_schema'
  -> AND TABLE_NAME LIKE '%summary%';



### InnoDB Buffer命中率

show status like 'innodb_buffer_pool_read%'; 

innodb_buffer_read_hits = (1 - innodb_buffer_pool_reads / innodb_buffer_pool_read_requests) * 100% 

innodb_buffer_read_hits>99%



### Binlog Cache 使用状况 

show status like 'Binlog_cache%'; 

如果Binlog_cache_disk_use值不为0 ，可能需要调大 binlog_cache_size大小

### Innodb_log_waits 量 

show status like 'innodb_log_waits'; 

Innodb_log_waits值不等于0的话，表明 innodb log  buffer 因为空间不足而等待 

### Tmp Table 状况(临时表状况) 

show status like 'Create_tmp%'; 

Created_tmp_disk_tables/Created_tmp_tables比值最好不要超过10%，如果Created_tmp_tables值比较大， 可能是排序句子过多或者是连接句子不够优化 



### Query Cache命中率 

show status like 'Qcache%'; 

Query_cache_hits = (Qcahce_hits / (Qcache_hits + Qcache_inserts )) * 100%; 

### QPS(每秒Query量)

数据库从启动uptime时间内所有的请求数量

QPS = Questions(or Queries) / seconds 

mysql > show  global  status like 'Question%'; 

### TPS(每秒事务量) 

TPS = (Com_commit + Com_rollback) / seconds 

show global status like 'Com_commit'; 

 show global status like 'Com_rollback'; 

#### SQL分析器

 show profile  cpu,block io for query

异常标志：

converting HEAP to MyISAM  查询结果太大，内存不够用，把数据搬到磁盘

Creating tmp table：创建临时表

Copying to tmp table on disk  把内存中临时变量复制到磁盘

locked

### SQL优化

exist/in

如果主查询数据集大，使用in

如果子查询的数据集大，使用exist

慢查询阈值：10s 默认值

开启sql全局日志记录：

show global  like '%general_log%'

set global general_log=1   开启全局日志

set global log_output=‘table’  以表格形式记录日志

全局记录仅仅用于调优，开发过程中关闭，记录的sql会存储在mysql.general_log

加读锁

lock table table_lock read

当前会话中，对A表加了读锁，则该会话可以对A表进行读操作，不可进行写操作，对A表之外的其他的表 不可读；其他会话对A表可以读取，但是不能写操作，必须等当前会话放弃读锁

加写锁：

lock table table_lock write

当前会话可以对该表做增删改查操作，但不能在操作其他表，其他会话也不能操作这个表

### MYSQL高速缓存分析

MYSQL的查询缓存用于缓存select查询结果，并在下次接收到同样的查询请求时，不再执行实际查询处理而直接返回结果，提高查询的速度，使查询性能得到优化，前提条件是你有大量的相同或相似的查询且很少改变表里的数据。

query_cache_size：设置为具体的大小，最好为1024倍数，参考值32M

query_cache_type：控制缓存类型，必须设置为数字（0：禁用,1：缓存所有结果,2:只缓存在select语句通过的sql）

show variables like ‘%query_cache%';

Qcache_lowmem_prunes变量的值来检查是否当前的值满足你目前系统的负载

Qcache_free_blocks：查询缓存中目前还剩多少blocks，如果值比较大，说明查询缓存中的内存碎片过多了，可能在一定的时间进行整理

Qcache_hits:表示有多少次命中缓存。我们主要可以通过该值来验证我们的查询缓存的效果。数字越大，缓存效果越理想

Qcache_inserts: 表示多少次未命中然后插入，即新来的SQL请求在缓存中未找到，不得不执行查询处理，执行查询处理后把结果insert到查询缓存中。这样的情况的次数，次数越多，表示查询缓存应用到的比较少，效果也就不理想

Qcache_lowmem_prunes:该参数记录有多少条查询因为内存不足而被移除出查询缓存。通过这个值，用户可以适当的调整缓存大小

