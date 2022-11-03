扫描方式：

主动探测：Scan

被动监听：Sniff

抓包：Capture

NMAP扫描：nmap  【-p 端口  】 -s 域名



| 参数 | 类型                |                              |
| ---- | ------------------- | ---------------------------- |
| -sS  | TCP SYN扫描（半开） |                              |
| -sT  | TCP连接扫描         | 默认                         |
| -sU  | UDP扫描             |                              |
| -sP  | ICMP扫描            |                              |
| -A   | 目标系统全面分析    | 复合扫描：检查系统，软件版本 |
|      |                     |                              |
|      |                     |                              |

NMAP 脚本扫描：

脚本目录：/usr/share/namp/scripts/

sudo  nmap  --script=脚本名称   ip地址 -p 端口

| 脚本                | 类型 | 作用                   |
| ------------------- | ---- | ---------------------- |
| ftp-anon            | ftp  | 测试ftp匿名登录        |
| ftp-syst            | ftp  | 测试系统信息           |
| ftp-vsftpd-backdoor | ftp  | 测试后门漏洞           |
| ftp-brute           | ftp  | 暴力破解               |
| ssh-brute           | ssh  | ssh暴力破解            |
| http-methods        | http | 测试支持http的访问方式 |
| http-sql-injection  | http | 测试SQL注入风险        |

#### john工具

根据已知的密文反向求明文数据。

傻瓜破解：sudo  john  --single  /etc/shadow

字典暴力破解：john  /etc/shadow

显示密码：sudo john --show /etc/shadow

建立密码本：sudo  john --worlist=字典文件  /etc/shadow

### 抓包

工具：tcpdump

tcpdump  选项  过滤条件

| 选项 | 作用                     |                |
| ---- | ------------------------ | -------------- |
| -i   | 监控网卡监控             | 默认第一块网卡 |
| -A   | 转换为ASCII码            |                |
| -w   | 将数据信心保存到指定文件 |                |
| -r   | 从指定文件读取包信息     |                |
| -c   | 自定义抓包个数           |                |
| -nn  | 不解析域名               | 默认TCP解析    |

| 过滤条件 |                                               | 命令：        |
| -------- | --------------------------------------------- | ------------- |
| 类型     | host net  port portrange（端口范围：600-800） | tcpdump  host |
| 方向     | src dst                                       | tcpdump src   |
| 协议     | tcp udp ip wlan arp                           | tcpdump  ip   |
| 组合条件 | and or not                                    |               |

