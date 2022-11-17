# mysql数据库运维知识

## mysql数据库集群实战

mysql数据库优化方向:高可用、主从复制、拆分库、拆分表、读写分离、

### 数据库主从复制

解决问题：

数据分布

负载均衡

数据备份，保证数据安全

高可用和容错性

读写分离，缓解数据库压力

mysql复制模式：

主从复制：主库授权从库连接。读取binlog日志并更新到本地数据库过程，主库写数据后，从库自动更新同步数据

主主复制（负载均衡）：主从相互授权连接，读取对方的binlog日志并更新到本地数据库过程中，保证彼此数据一致



## 1、开放数据库远程登录功能

方式1：改表：user  修改root的值为‘%’

select  user，host from user；

update user set host=‘%’ where user=‘root’

刷新：flush privileges

方式2：授权

grant all priviliges on *.*To 'root' ip地址 identified by ‘root’ with grant option；

## 2、数据库管理

1常规备份

 mysqldump  -h IP地址 -u用户 -p密码 数据库 > 目录/bak.sql

2 仅仅备份表结构:

mysqldump -no-data   -databases 数据库名...... > bak.sql

3 备份带删除表功能的sql脚本

mysqldump   -–add-drop-table -uusername -ppassword databasename > backupfile.sql

4 备份所有数据库

mysqldump -all-databases > allDatabase.sql

5 备份单个表

mysqldump  -u root  -p  数据库名  表名 > 你要保存的sql文件（加位置）

6还原数据库

mysql -hhostname -uusername -ppassword databasename < backupfile.sql

7 部分列赋予权限

grant select(id, se, rank) on testdb.apache_log to dba@localhost; 

注意:

数据库恢复或还原速度

数据库丢失允许程度

逻辑备份:导出sql文件,mysqldump  mydumper

物理备份:备份binlog.基于slave的rsync,copy,tar

## 数据库表分区

读写分离分散数据库读写操作压力,分库分表酚酸存储压力,常见的分区方式是按主键分区

分区算法:

#### hash(filed):

相同的输入得到相同的输出,比较适用于整型字段


create table article(

id int auto_increment PRIMARY KEY,

title varchar(64),

content text

)PARTITION by HASH(id) PARTITIONS 10

#### key(filed):

和hash性质一样,`key`是**处理字符串**的，比`hash()`多了一步从字符串中计算出一个整型在做取模操作

create table article_key(

id int auto_increment,

title varchar(64),

content text,

PRIMARY KEY (id,title)	-- 要求分区依据字段必须是主键的一部分

)PARTITION by KEY(title) PARTITIONS 10

## range(field)

条件分区,按照数据条件范围分散到不同区中,条件运算符:less than

create table article_range(

id int auto_increment,

title varchar(64),

content text,

created_time int,	-- 发布时间到1970-1-1的毫秒数

PRIMARY KEY (id,created_time)	-- 要求分区依据字段必须是主键的一部分

)charset=utf8

PARTITION BY RANGE(created_time)(-- 注意：分区的定义顺序依照created_time数值范围从小到大，不能颠倒

PARTITION p201808 VALUES less than (1535731199),	-- select UNIX_TIMESTAMP('2018-8-31 23:59:59')

PARTITION p201809 VALUES less than (1538323199),	-- 2018-9-30 23:59:59

PARTITION p201810 VALUES less than (1541001599)	-- 2018-10-31 23:59:59

);

## list(field)

条件分区 按照列表值分区 (in (值列表)),适用于判断布尔值

create table article_list(

id int auto_increment,

title varchar(64),

content text,

status TINYINT(1),	-- 文章状态：0-草稿，1-完成但未发布，2-已发布

PRIMARY KEY (id,status)	-- 要求分区依据字段必须是主键的一部分

)charset=utf8

PARTITION BY list(status)(

PARTITION writing values in(0,1),	-- 未发布的放在一个分区	

PARTITION published values in (2)	-- 已发布的放在一个分区

);

## 数据库实践:

### 命令：show status like '%下面变量%';

| 变量                     | 解释                                                         |
| ------------------------ | ------------------------------------------------------------ |
| aborted_clients          | 由于客户没有正确关闭连接已经死掉，已经放弃的连接数量         |
| aborted_connects         | 试已经失败的MySQL服务器的连接的次数                          |
| connections              | 试图连接MySQL服务器的次数。                                  |
| created_tmp_tables       | 当执行语句时，已经被创造了的隐含临时表的数量。               |
| delayed_insert_threads   | 正在使用的延迟插入处理器线程的数量。                         |
| delayed_writes           | 用INSERT DELAYED写入的行数。                                 |
| delayed_errors           | 用INSERT DELAYED写入的发生某些错误(可能重复键值)的行数       |
| flush_commands           | 执行FLUSH命令的次数。                                        |
| handler_read_first       | 请求读入表中第一行的次数。                                   |
| handler_read_key         | 请求数字基于键读行。                                         |
| handler_read_next        | 请求读入基于一个键的一行的次数。                             |
| handler_read_rnd         | 请求读入基于一个固定位置的一行的次数。                       |
| handler_update           | 请求更新表中一行的次数。                                     |
| handler_write            | 请求向表中插入一行的次数。                                   |
| key_blocks_used          | 用于关键字缓存的块的数量                                     |
| key_read_requests        | 请求从缓存读入一个键值的次数                                 |
| key_reads                | 从磁盘物理读入一个键值的次数                                 |
| key_write_requests       | 请求将一个关键字块写入缓存次数                               |
| key_writes               | 将一个键值块物理写入磁盘的次数。                             |
| max_used_connections     | 同时使用的连接的最大数目                                     |
| open_tables              | 打开表的数量                                                 |
| not_flushed_key_blocks   | 在键缓存中已经改变但是还没被清空到磁盘上的键块。             |
| open_files               | 打开文件的数量                                               |
| open_streams             | 打开流的数量(主要用于日志记载）                              |
| opened_tables            | 已经打开的表的数量。                                         |
| questions                | 发往服务器的查询的数量                                       |
| slow_queries：           | 当前慢查询数量                                               |
| not_flushed_delayed_rows | 在INSERT DELAY队列中等待写入的行的数量                       |
| threads_connected        | 当前打开的连接的数量                                         |
| threads_running          | 不在睡眠的线程数量                                           |
| Uptime                   | 服务器工作了多少秒                                           |
| table_locks_waited       | 查看不能立即获得的表的锁的次数。如果该值较高，并且有性能问题，你应首先优化查询，然后拆分表或使用复制。 |
| table_locks_immediate    | 查看立即获得的表的锁的次数                                   |
| threads_created          | 查看创建用来处理连接的线程数。如果Threads_created较大，你可能要增加thread_cache_size值 |
| com_xxx                  | xxx:表示select  insert  delet update 等，查看当前数据操作个数 |
|                          |                                                              |

## innodb引擎全局变量参数优化

| 参数                            | 参数值                | 备注                                                         |
| ------------------------------- | --------------------- | ------------------------------------------------------------ |
| innodb_buffer_pool_size         | 物理内存80%左右       | 纯数据库服务器，可以通过调整命中率来优化，值为innodb_buffer_pool_chunk_size* innodb_buffer_pool_instances的倍数 |
| innodb_buffer_pool_instances    | 数据库实例            | 该值更改 会影响innodb_buffer_pool_size的大小，最大值：64     |
| innodb_buffer_pool_chunk_size   | 128M                  | 该值更改 会影响innodb_buffer_pool_size的大小                 |
| innodb_additional_men_pool_size | 100M（32G物理内存）   | 默认值                                                       |
| innodb_log_buffer_size          | 不超过32M             | 默认值8M，日志写入磁盘前的缓存大小                           |
| innodb_flush_log_trx_commit     | 1(对数据插入影响较大) | 默认值1  0：log buffer中的数据将以每秒一次的频率写入到log file；          1：在每次事务提交的时候将log_buffer 中的数据都会写入到 log_file                    2：事务提交会触发log_buffer到log_file的刷新，但并不会触发磁盘文件系统到磁盘的同步；插入1000数据所需时间：0<2(2s)<1(229s) |
| query_cache_size                | 32M                   | 默认值32M,SQL语句执行的结果集影响较大，256M已足够使用                                                                      通过show status like 'Qcache_%'                                                                                              计算命中率(Qcache_hits/(Qcache_hits+Qcache_inserts)*100)) |
| key_buffer_size                 | 256M(4GB物理内存)     | 更好的处理索引问题取决于key_reads / key_read_requests；未命中概率小于：1：100，1：1000，1：10000 |
| wait_timeout                    | 30                    | 数据库连接空闲时间，大量的连接会消耗内存资源，导致“Too many connections”提示，需要在一定时间断开“sleep”状态的进程 |
| interactive_time                | 30                    | 与wait_timeout一起使用,长连接保持时间                        |
| max_connections                 | 16384                 | 数据库连接的最大值，过多连接影响服务器性能                   |
| max_user_connections            | 10000                 | 每个数据库用户的最大连接，控制最大数据库的并行数，0表示无限制 |
| thread_concurrency              | CPU核数的2倍          |                                                              |
| 局部缓存                        |                       |                                                              |
| read_buffer_size                | 4M                    | 默认值4M                                                     |
| sort_buffer_size                | 4M                    | 默认4M MySql执行排序使用的缓冲大小。如果想要增加ORDER BY的速度 |
| read_rnd_buffer_size            | 8M                    | MySql会首先扫描一遍该缓冲，以避免磁盘搜索，提高查询速度，如果需要排序大量数据，可适当调高该值 |
| tmp_table_size                  | 16M                   | 默认值16M，提高联接查询效率                                  |
| record_buffer                   | 128K                  | 默认值                                                       |
|                                 |                       |                                                              |
| table_cache                     | 512                   | mysql手册上给的建议大小 是:table_cache=max_connections*n（n 表示联接表数量） |
| thread_cache_size               | 8                     | 默认值 8 服务器线程缓存 ，根据服务器内存来设置               |

备注：

当前连接生效：session级别修改变量 set session key=value；

所有下次连接都会生效：global级别：set global key=value；

### 查看mysql的全局变量：

show global variables;

### 查看特定的全局变量：

show variables like "%xxxx%"

### 查看进程状态

show full processlist;

| state值                        | 行为分析                                                     | 影响                                                         |
| ------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Checking     table             | 正在检查数据表                                               |                                                              |
| Closing tables                 | 正在将表中修改的数据刷新到磁盘中，同时正在关闭已经用完的表。 | 这是一个很快的操作，如果不是这样的话，就应该确认磁盘空间是否已经满了或者磁盘是否正处于重负中 |
| Connect Out                    | 从服务器正在连接主服务器                                     | 主从复制断开，试图重新建立连接                               |
| Copying to tmp table on disk   | 临时表由内存存储转为磁盘存储                                 | 由于临时结果集大于tmp_table_size                             |
| Create tmp table               | 创建临时表                                                   | :正在创建临时表以存放部分查询结果                            |
| deleting from main table       | 正在执行多表删除中的第一部分                                 | 刚删除第一个表                                               |
| deleting from reference tables | 正在执行多表删除中的第二部分                                 | 正在删除其他表的记录                                         |
| Flushing tables                | 正在执行FLUSH TABLES                                         | 等待其他线程关闭数据表                                       |
| Locked                         | 被其他查询锁住了                                             |                                                              |
| Sending data                   | 正在处理SELECT查询的记录，同时正在把结果发送给客户端         |                                                              |
| Sorting for group              | 正在为GROUP BY做排序                                         |                                                              |
| Opening tables                 | 正在尝试打开表                                               | 这个过程应该会很快，除非受到其他因素的干扰。例如，在执ALTER TABLE或LOCK TABLE语句行完以前，数据表无法被其他线程打开 |
| Removing duplicates            | 正在执行一个SELECT DISTINCT方式的查询                        |                                                              |
| Reopen table                   | 正尝试重新打开数据表                                         | 获得了对一个表的锁，但是必须在表结构修改之后才能获得这个锁。已经释放锁，关闭数据表 |
| Repair by sorting              | 正在排序以创建索引                                           | 修复指令                                                     |
| Searching rows for update      | 搜索符合条件的记录找出来以备更新                             | 必须在UPDATE要修改相关的记录之前就完成                       |
| Updating                       | 正在搜索匹配的记录                                           | 正在搜索匹配的记录，并且修改它们                             |
| Waiting for tables             | 该线程得到通知，数据表结构已经被修改了，需要重新打开数据表以取得新的结构 | 然后，为了能的重新打开数据表，必须等到所有其他线程关闭这个表。以下几种情况下会产生这个通知：FLUSH TABLES tbl_name, ALTER TABLE, RENAME TABLE, REPAIR TABLE, ANALYZE TABLE,或OPTIMIZE TABLE。 |
| waiting for handler insert     | 处理完所有待插入操作                                         |                                                              |



### 查看慢查询配置:

show variables like '%slow%'

log_slow_queries   是否开启慢查询

slow_launch_time  慢查询秒数

slow_query_log  开启慢查询日志

slow_query_log_file   慢查询日志存放目录



查看服务器资源消耗分析，数据来自information_schema库下的profiling表

show profile

查看所有的sql性能

SHOW PROFILES 

#查看指定sql性能分析，根据query_id查询
		show PROFILE ALL FOR QUERY 183 limit 10

### 数据库高可用方案

LVS+keepalived

BaseStone@2021