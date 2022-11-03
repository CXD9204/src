# docker常用命令:

docker pull //拉取镜像

docker search 镜像名称

docker images //查看镜像

docker ps //查看所有正在运行容器

docker ps -a //查看所有容器 

docker ps -a -q // 查看所有容器ID

docker start $(docker ps -a -q) //启动所有停止的容器

docker stop $(docker ps -a -q) //停止所有容器

docker rm $(docker ps -a -q) //删除所有容器

docker rmi $(docker images -q) //删除所有镜像

docker attach containerID //进入已启动容器，退出后台停止

docker exec -it containerID /bin/bash //进入已启动容器，退出后台运行

docker cp /export/output/ containerID:/opt/ //宿主机向容器拷贝文件

docker cp containerID:/opt/ /export/output/ //容器向宿主机拷贝文件

docker  logs  -f  容器ID：查看docker的运行日志

### 镜像备份（导入/导出）

docker save  镜像名称：镜像标签  -o 备份文件名（tar格式）

docker export  自定义容器tar文件    容器ID 

docker镜像恢复：

docker load -i  备份文件名称

docker  import  容器tar包文件   容器名：版本

docker save与export区别  load与import区别

| export与save                                                 | load与import                                                 |      |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| save：保存的是容器的镜像，即使参数是容器ID，保存的依旧是容器背后的镜像文件 | load：导入镜像，且不能对镜像重命名                           |      |
| export：保存的是容器快照，一般导出的文件比save导出的文件小一点 | import：将容器导入后变成一个镜像，而不是恢复成容器，且可以指定镜像名称 |      |
|                                                              |                                                              |      |

### docker开机自启动

docker容器开机自启，设置运行内存

docker run  --restart=always  --name  别名  -m 512m --memory-swap 1G 容器镜像  

### docker update 修改容器参数

| 名称                  | 描述                                                       |
| :-------------------- | :--------------------------------------------------------- |
| `--blkio-weight`      | 阻塞IO (相对权重)，介于10到1000之间，0表示禁用（默认禁止） |
| `--cpu-period`        | 限制CPU CFS（完全公平的调度程序）期限                      |
| `--cpu-quota`         | 限制CPU CFS（完全公平的调度程序）配额                      |
| `--cpu-rt-period`     | `API 1.25+`，将CPU实时时间限制为微秒                       |
| `--cpu-rt-runtime`    | `API 1.25+`，将CPU实时运行时间限制为微秒                   |
| `--cpu-shares`, `-c`  | CPU份额（相对权重）                                        |
| `--cpus`              | `API 1.29+`，CPU数量                                       |
| `--cpuset-cpus`       | 允许执行的CPU（0-3，0,1）                                  |
| `--cpuset-mem`        | 允许执行的MEM（0-3，0,1）                                  |
| `--kernel-memory`     | 内核内存限制                                               |
| `--memory-swap`       | 交换限制等于内存加交换，“-1”以启用无限交换                 |
| `--memory-reservatio` | 内存软限制                                                 |
| `--memory`, `-m`      | 内存限制                                                   |
| `--pids-limit`        | `API 1.40+`，调节容器pids限制（-1表示无限制）              |
| `--restart`           | 容器退出时重新启动策略以应用                               |











### docker容器数据持久化

Bind mount和Docker Manager Volume的区别

> - Bind mount数据持久化的方式，如果是挂载本地的一个目录，则容器内对应的目录下的内容会被本地的目录覆盖掉，而Docker Manager Volume这种方式则不会，不管哪种方式的持久化，在容器被销毁后，本地的数据都不会丢失。
> - 使用“-v”选项挂载时，Bind mount明确指定了要挂载docker host本地的某个目录到容器中，而Docker Manager Volume则只指定了要对容器内的某个目录进行挂载，而挂载的是docker host本地的哪个目录，则是由docker来管理的。

Bind mount——数据卷容器：--volumes-from方式实现数据持久化

数据持久化: docker run -it  --name 别名  -v 宿主主机绝对路径:/容器内目录  镜像名称

### Docker Manager Volume实现数据持久化

数据持久化: docker run -it --name  别名  -v 容器目录  镜像名称

查看镜像内容:docker inspect 容器名称

### 数据卷容器

通过命名的`容器挂载数据卷,其他容器通过挂载父容器实现数据共享,挂在数据卷的容器,成为数据卷容器

1 启动父容器:docker run  -it --name  镜像

2继承父容器运行:docker run -it  --name  别名  --volumes-from 父容器   镜像



## dockerfile文件编写

1 、手动编写一个dockerfile文件

2 、编写完毕后,使用docker build命令执行,建立一个自定义镜像

docker  build -f 文件的绝对路径  -t  镜像名称:版本  .

3 、run 运行自定义的镜像文件

docker run -it 镜像名称:版本

4 history 查看dockerfile运行过程

docker  history  镜像名称:版本

基础语法：

1 每条保留字指令必须师大写字母且后面要有一个参数

2 指令按照从上到下 顺序执行

3 # 表示注释

4：每条指令都会建立一个新的镜像，并对镜像进行提交

dockerfile保留字 

| 保留字     | 解释                                                         |      |
| ---------- | ------------------------------------------------------------ | ---- |
| FROM       | 先择定制的镜像都是基于from的镜像                             |      |
| MAINTAINER |                                                              |      |
| RUN        | 用于执行后面跟着的活动命令                                   |      |
| EXPOSE     | 对外的映射端口                                               |      |
| WORKDIR    | 指定文件的工作目录                                           |      |
| ENV        | 构建镜像过程中的环境变量                                     |      |
| VOLUME     | 容器数据卷，保持数据持久化 在启动容器时忘记挂载数据卷，会自动挂载到匿名卷。 |      |
| CMD        | 指定容器启动执行的命令，dockerfile文件可以有多个cmd 命令 但只有最后一个有效 |      |
| ADD        | 拷贝和解压缩                                                 |      |
| COPY       | 从上下文目录中复制文件或则目录到容器指定的路径               |      |
| ENTRYPOINT | 指定容器启动执行的命令，不会覆盖命令，只会追加               |      |
| ONBUILD    | 用于延迟构建命令的执行。执行新镜像的dockerfile构建镜像是，会调用该命令 |      |

#### 本地镜像push到阿里云



**s9q_vum9HxX1KwxobQpZ3zZsq0fWY5wOTCMFCtFEAJQIAn6Ud6FG3VEPC3jf1uH0vvjwf_72rRfnppga6oCS3w==**