

# Linux7.5离线手动安装mysql5.7

### 1、查询系统是否自带Mariadb数据库

<!--MariaDB是MySQL源代码的一个分支，采用Aria存储引擎，项目代码多改编于MySQL6.0版本，为避免对安装mysql5.7有影响 先卸载MariaDB-->

```
rpm -qa|grep mariadb
```

### 2、删除系统自带的 mariadb数据库

```
 rpm -e --nodeps mariadb-libs-5.5.44-2.el7.centos.x86_64
```

### 3、到/usr/local/目录 新建mysql文件夹

mkdir  /usr/local/mysql

cd /usr/local/mysql

### 4、下载mysql 5.7的tar包到mysql目录或者rpm文件

实际工作环境可能连接不到外网，需要提前下载到U盘

安装包下载网址：https://downloads.mysql.com/archives/community/

### 5、下载rmp文件

wget -c https://downloads.mysql.com/archives/get/p/23/file/mysql-community-sver-5.7.30-1.el7.x86_64.rpm

安装mysql5.7所需要的的依赖包

![image-20200828155303541](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20200828155303541.png)

![image-20200828151744147](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20200828151744147.png)

标注1 tar包里面包含安装mysql的其他依赖组件。

标注2、3 :rpm安装包 虽然使用systemctl status mysql.service 可以看到mysql服务启动，但登录会提示mysql命令无效，原因是缺少其他依赖组件

遇坑经验：在其他依赖包没有安装的情况下  多次安装，会导致rpm损坏 需要自己重新下载，



### 6、安装mysql服务器

rpm -ivh --force --nodeps mysql-community-server-5.7.30-1.el7.x86_64.rpm

force：强制安装

nodeps：不检查依赖关系

### 7、查看mysql服务 

systemctl status mysqld.service 

### 8、启动mysql服务

systemctl start mysqld.service 

### 9、从安装日志 查看 root用户的初始密码

grep "password" /var/log/mysqld.log

### 10、登录mysql

mysql -uroot -p

输入初始密码：

![image-20200828155036216](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20200828155036216.png)

bash: mysql: 未找到命令

### 10、登录成功后修改mysql的root初始密码

```
set PASSWORD = PASSWORD('123456')
```

### 11、尝试再一次登录

### 12 mysql性能优化：打开etc目录下编辑my.cnf文件  填写相关的性能优化参数

vi /etc/mycd my.cnf

### 13、设置mysql服务开机自启动

方式1： systemctl enable mysqld@.service 

方式2：编译/ect/rc.local文件 追加：systemctl start mysql.service

### 14开放3306端口

