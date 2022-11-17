## 基于双节点的主主复制环境

| 主机1(主)              | 主机2(从)              |      |
| ---------------------- | ---------------------- | ---- |
| 192.168.177.132        | 192.168.177.133        |      |
| 数据库:mysql5.7        | 数据库:mysql5.7        |      |
| 数据库密码:Am@19920417 | 数据库密码:Am@19920417 |      |

搭建思路:先搭建主从复制,然后由主从复制转为双主机复制

### 主库操作



create user mts identified by "M@s19920417";

grant all privileges on *.* to "mts" @ "%" identified by "密码"

grant replication slave on *.* to 'mts'@'%' identified by 'Am@19920417';

### 从库操作

change master to

master_host='192.168.177.132',            

master_user='mts',							

master_password='M@s19920417',  

master_log_file='mysql-bin.000004',   

master_log_pos= 8515;	

### 主主复制

从库停止复制主库内容

stop slave

创建账号:create user ‘mts’@’ 10.196.177.133’ identified with ‘mysql_native_password’ M@s19920417’; 

账户赋予权限:grant all privileges on *.* to "mts" @ "%" identified by "密码"

赋予复制权限:grant replication slave on *.* to 'mts'@'%' identified by 'M@s19920417';

查看当前二进制文件和位置

show master status

主库执行复制操作

change master to

master_host='192.168.177.133',            

master_user='mts',							

master_password='M@s19920417',  

master_log_file='mysql-bin.000001',   

master_log_pos=522411;	



## 基于Keepalived搭建高可用环境

ifconfig ens33:1 192.169.177.10 broadcast 192.168.177.255 netmask 255.255.255.0 up

route add -host 192.168.177.10 dev ens33:1

