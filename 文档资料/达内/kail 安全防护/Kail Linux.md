查看网卡：sudo nmcli connection show

nmcli connection modify "Wired connection 1 " ipv4.method manual ipv4.addr 192.168.177.203/24 autoconnection yes

### 渗透测试

#### 端口扫描：NMAP

脚本目录：/usr/share/namp/scripts/

sudo  nmap  --script=脚本名称   ip地址 -p 端口

| 参数 | 类型                |                              |
| ---- | ------------------- | ---------------------------- |
| -sS  | TCP SYN扫描（半开） |                              |
| -sT  | TCP连接扫描         | 默认                         |
| -sU  | UDP扫描             |                              |
| -sP  | ICMP扫描            |                              |
| -A   | 目标系统全面分析    | 复合扫描：检查系统，软件版本 |
|      |                     |                              |
|      |                     |                              |

| 脚本                | 类型 | 作用                        |
| ------------------- | ---- | --------------------------- |
| ftp-anon            | ftp  | 测试ftp匿名登录             |
| ftp-syst            | ftp  | 测试系统信息                |
| ftp-vsftpd-backdoor | ftp  | 测试后门漏洞                |
| ftp-brute           | ftp  | 暴力破解                    |
| ssh-brute           | ssh  | ssh暴力破解（或者指定字典） |
| http-methods        | http | 测试支持http的访问方式      |
| http-sql-injection  | http | 测试SQL注入风险             |

![image-20210721210407702](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20210721210407702.png)

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



#### 协议分析(抓包)：tcpdump ,WireShark 

### Linux安全防护：

| 工具        | 参数                              |                                                        |
| ----------- | --------------------------------- | ------------------------------------------------------ |
| chage       | -d 0  -E yyyy-mm-dd  指定失效日期 |                                                        |
| passwd      | 锁定：-l  解锁：-u  看状态：-S    |                                                        |
| issue(文件) | 伪登录提示                        | 登录信息 修改里面的内容  编辑/etc/issue,/etc/issue.net |
|             |                                   |                                                        |
|             |                                   |                                                        |

#### 文件属性控制：

chattr，lsattr

控制方式：

属性i：不可变

属性a：尽可追加

#### mount 挂载属性（fstab）

noexec 不可执行程序，可以加载boot目录下

noatime：不更新文件的访问时间

#### 禁止非必要系统服务

使用systemctl  chkconfig

cpus.service 打印机服务

postfix：邮件服务

networkManager.service  网络管理服务

firewalld  防火墙（iptables代替）

bluetoth.service 蓝牙服务

autofs.service 自动挂载服务

pcscd.service  智能卡设备资源管理

### 安全检测

### 密码安全

### 反向工程

### 加密

生产秘钥：gpg  --gen-key

查看秘钥：gpg --list-keys

导出公钥：gpg  --export 

加密：gpg  -e -r userb attr.txt  

![image-20210723215333659](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20210723215333659.png)

导入公钥：gpg   --import 

![image-20210723215222849](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20210723215222849.png)

签名认证：



### 系统日志审计

参考链接：https://blog.csdn.net/weixin_44908159/article/details/108314421

基于事先设定的规则，记录系统可能发生的事件，仅仅提供记录的功能，无法提供保护的工作

安装：yum install -y audit

auditctl  -s  查看状态

auditctl  -l   查看审计规则

auditctl  -D  删除审计

使用格式：auditctl  -w 文件或目录  -p 审计监控（r，w，x，a） -k  key_name

编译临时审计：auditctl  -w  /etc/passwd  -p wa  -k  passwd_change

创建永久审计：

*vim  /etc/audit/rules.d/audit.rules*

 -w /etc/passwd -p wa -k passwd_changes 

-w /usr/sbin/fdisk -p x -k partition_disks

查看审计日志：

ausearch  -k  key_name

![image-20210725003425323](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20210725003425323.png)

### Iptables 表,链结构 

永久保存规则：iptables-save  

扩展iptables 规则：iptables  -m  规则项目

| 项目      |      |                    |
| --------- | ---- | ------------------ |
| multiport |      | 多端口             |
| iprange   |      | IP范围             |
| connlimit |      | 限制链接的最大个数 |
| limit     |      | 指定速率           |

 iptables -A INPUT -p tcp --dport 22 -m iprange --src-range  192.168.4.200-192.168.4.254 -j ACCEPT

#### NAT转换原理

POSTROUNT 路由后的转换，外网的IP地址

 nmcli connection modify ens37 ipv4.method manual ipv4.addresses  192.168.2.110/24 connection.autoconnect yes