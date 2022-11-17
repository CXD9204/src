2安装相应的工具wget gzip tar

yum install -y wget gzip tar make gcc 编译安装wget工具

**3****使用wget安装yum Repository到本地缓存

wget -c http://dev.mysql.com/get/mysql57-community-release-el7-10.noarch.rpm

4服务器包信息下载到本地缓

Yum makecache

5安装yum Repository

yum -y install mysql57-community-release-el7-10.noarch.rpm

安装mysql服务器

```
yum -y install mysql-community-server
```

 

**6****启动mysql7运行**

systemctl start mysqld.service或者service mysqld start

7查看MYSQL运行情况

systemctl status mysqld.service

**8****查询数据库初始密码**

```
grep "password" /var/log/mysqld.log(密码`:hdlH+=CIw9<q )
修改root用户密码
ALTER user 'root'@'%' IDENTIFIED BY 'Am@19920417'
```

```
或者update user set password=password("Am@19920417") where user='root';
或者:set PASSWORD = PASSWORD('Am@19920417')
设置密码不符合条件
 
修改密码的设置条件
```

**查看密码设置规则**

```
SHOW VARIABLES LIKE 'validate_password%'

密码的长度是由validate_password_length决定
```

如果不需要密码策略，可my.cnf文件中添加如下配置禁用：
 validate_password = off 修改完后记得需要重新启动MySQL服务


 validate_password相关参数说明：
 validate_password_dictionary_file：密码策略文件，策略为STRONG才需要
 validate_password_length：密码最少长度
 validate_password_mixed_case_count：大小写字符长度，至少1个
 validate_password_number_count ：数字至少1个
 validate_password_special_char_count：特殊字符至少1个上述参数是默认策略MEDIUM的密码检查规则。
 validate_password_policy：密码策略，默认为MEDIUM策略，共有如下三种密码策略：

策略 检查规则
 0 or LOW Length
 1 or MEDIUM Length; numeric, lowercase/uppercase, and special characters
 2 or STRONG Length; numeric, lowercase/uppercase, and special characters; dictionary file

```
 
```

**开放3306端口(通用开放8080端口)**

firewall-cmd --permanent --zone=public --add-port=3306/tcp 

firewall-cmd --reload 

firewall-cmd --zone=public --query-port=9999/tcp 

systemctl start firewalld



# mysql5.7的my.cnf配置以及性能优化

<!--#InnoDB以下优化参数是参考mysql5.6性能优,部分配置参数导致虚拟机内的mysql5.7无法重新启动,无效配置前有标=标志符号"#"--> 

innodb_log_files_in_group = 4                          - -指定4个日值组
innodb_buffer_pool_chunk_size = 1024M     --
innodb_buffer_pool_instances = 10                 --缓存池实例个数为10
innodb_buffer_pool_size = 500M    --InnoDB缓冲池设置为10240M mysql在内存中可缓存10240M数据和索引
innodb_log_file_size = 128M                 --InnoDB日志文件大小为128M
innodb_log_buffer_size = 8M                --Innodb的日志缓冲大小为8M
innodb_flush_log_at_trx_commit = 1   --控制事务提交方式 1:提交事务到日志缓冲区,同步将缓冲区日志写入物理日志文件 
innodb_lock_wait_timeout = 50            --设置锁等待的时间是50s
innodb_file_per_table = 1                       --每张表在独立的物理文件中存储数据和索引 默认关闭
innodb_open_files = 2000                      --限制Innodb可以打开的表数据为2000

max_connections = 512                          --mysql允许的最大用户连接数

innodb_flush_method=O_DIRECT         -- 设置innodb与linux打交道的IO模型围殴O_DIRECT

innodb_max_dirty_pages_pct=85         --设置innodb的脏页百分比  默认90  太大需要致换的数据页太多

innodb_thread_concurrency=2             --innodb内核的线程数量  默认值8 计算方式= 核心数x2

#innodb_additional_mem_pool_size=10M  --缺省值1M  存储数据字典和其他内部数据结构的内存池大小  基于5.6的优化  在5,7中 数据库不能重新启动

innodb_io_capacity=3000     i               --刷新脏页数量和合并插入数量  

innodb_io_capacity_max=6000

innodb_use_native_aio=ON                --设定InnoDB可以使用Linux的异步I/O子系统

innodb_read_io_threads=1000           --可调整的读请求的后台线程数

innodb_write_io_threads=1000          --可调整的写请求的后台线程数

innodb_purge_threads=1                    --随机读缓冲区大小

#####Binary_log##############

#保证复制的InnoDB事务持久性和一致性

#sysc_binlog=1                                 B         --同步写入磁盘  安全性高

#sync_relay_log=1         

#启用此两项,可用于实现在崩溃时保证二进制及从服务器安全的功能                     

relay-log-info-repository=TABLE
master-info-repository=TABLE

#设置清除日志时间

expire_logs_days=7

#行复制

binlog_format=ROW

#mysql数据库事务隔离级别

transaction-isolation=READ-COMMITTED

##################cache############################

character-set-server=utf8                 --设置编码格式
explicit_defaults_for_timestamp=true   --\#开启查询缓存

query_cache_size=512M                       --使用查询缓冲  大小512M

record_buffer_size=16M                       --每个线程扫描每张表分配16M的缓冲

read_rnd_buffer_size=16M                   --随机读取缓冲大小16M

sort_buffer_size=16M                            --每个需要进行排序的线程分配该大小的一个缓冲区

#table_cache=128M                                  --表高速缓存大小 

thread_cache_size=80                             --复用保存在缓存中的线程数量

#thread_concurrency=2                            --默认值8   CPU核心数*2

wait_timeout = 5                                     --最大请求连接数  4G一般选择5-10

table_open_cache = 512                        --缓存数据文件的描述符相关信息大小  

 max_allowed_packet = 16M                --网络包大小

thread_stack=256k                                 --限定用于每个数据库线程的栈大小

max_heap_table_size=256M                --内部内存临时表的最大值,每个线程都要分配

binlog_cache_size = 2M                        --事务过程中容纳二进制日志SQL语句的缓存大小

interactive_timeout=7200                    --一个交互连接在被服务器在关闭前等待行动的秒数 *默认28800  调优7200*                 

sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION

lower_case_table_names=1

event_scheduler = 1

innodb_temp_data_file_path = ibtmp1:12M:autoextend:max:50G