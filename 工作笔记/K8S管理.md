官网指南：https://www.kubernetes.org.cn/kubernetes-labels

## 组件介绍

![image-20210620164518770](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20210620164518770.png)

- etcd 一个高可用的K/V键值对数据库，存储k8s的元数据和服务发现系统
- flannel 实现跨主机的容器网络的通信
- kube-apiserver 提供kubernetes集群的API调用
- kube-controller-manager 确保集群服务
- kube-scheduler 负责集群内部资源调度，调度容器，分配到Node
- kubelet 在Node节点上按照配置文件中定义的容器规格启动容器
- kube-proxy 提供网络代理服务



k8s集群添加节点

kubeadm join 192.168.177.200:6443   --token 28ee89.qm8he23p5gikr7gc --discovery-token-ca-cert-hash sha256:e09541eda66a35dac7d6c9e38697146df1b25b3cb0b092b1041b2c7b857094aa





kubeadm init --kubernetes-version=v1.15.12 --image-repository registry.aliyuncs.com/google_containers  --pod-network-cidr=10.254.0.0/16 --service-cidr=10.254.0.0/16

kubeadm join 192.168.177.200:6443 --token d6k0ez.v5sxuy0s8swknsib \
    --discovery-token-ca-cert-hash sha256:bb45e1ab361908a932552a0387eb4743261f11d7888298f34fdfa0b9cb2dc89c 

### 问题汇总：

#### 重启启动后：

拒绝连接：The connection to the server 192.168.177.200:6443 was refused - did you specify the right host or port?

原因：kubelete没有启动，kubelet负责管理集群容器正常启动



错误提示：/proc/sys/net/ipv4/ip_forward contents are not set to 1

原因：Linux系统默认是禁止数据包转发的，配置Linux系统的ip转发功能

临时：echo "1" > /proc/sys/net/ipv4/ip_forward

永久：/etc/sysconfig/network脚本中添加 FORWARD_IPV4="YES"

node节点处于notReady状态：node没有安装flannel网络组件



### 相关组件

#### Yaml资源清单

语法：

缩进不允许使用tab键  只允许使用空格

缩进空格数目不重要，相同层数左侧对其即可

#标识注释

------

Yaml支持的数据结构

对象：键值对的集合，又称为映射 哈希 字典

纯量：单个的 不可分割的值

------

字段解释说明：

| 参数                              | 字段类型 | 说明                                                         |
| --------------------------------- | -------- | ------------------------------------------------------------ |
| version                           | string   | 指定k8s的API版本类型，可以使用kubuctl api-version 命令查询 一般都是v1 |
| kind                              | string   | 指定yaml文件定义的资源类型和角色 例如pod                     |
| metadata                          | Object   | 元数据对象，固定值就写matedata                               |
| metadata.name                     | string   | 元数据对象的名字 自定义                                      |
| metadata.namespace                | string   | 元数据对象的命名空间 自定义                                  |
| spec                              | Obesct   | 详细定义对象，固定值就写spec                                 |
| spec.containers[]                 | list     | 详细定义对象的容器列表定义                                   |
| spec.containers[].name            | string   | 容器的名字，可随机生成                                       |
| spec.containers[].image           | string   | 容器需要使用的镜像名称                                       |
| 以上是yaml配置文件必须存在的属性  |          |                                                              |
| spec.containers[].imagePullPolicy | string   | 定义镜像的拉取策略：Always ：每次尝试拉取镜像，Never ：仅仅使用本地镜像，IfNotPresent ：本地存在则使用本地镜像，否则在线拉取。默认都是always |
| spec.containers[].command[]       | list     | 指定容器的启动命令，数组可以指定多个，不指定则使用镜像打包的启动命令 |
| spec.containers[].args[]          | list     | 容器启动的命令参数                                           |
| spec.containers[].workingDir      | string   | 容器的工作目录                                               |
| spec.containers[].volumeMount[]   | list     | 指定容器内部存储配置                                         |
|                                   |          |                                                              |



#### 名称空间资源

工作负载资源：

Pod   replicaset  deployment statefulset  damemonset job  cronjod

服务发现以及负载均衡资源

service  ingress

配置与存储资源

volume  csi容器存储接口

特殊类型存储卷

configMap（配置中心使用的资源类型）、secret（敏感数据）

集群级资源：Namespace  Node Role  ClusterRole  RoleBinding  ClusterRolebinding

元数据资源类型：HPA、 PodTemplate 、Limitrange

##### Pod

k8s管理的最小单位

生命周期：

initC：总是运行到成功完成为止且会在下一个容器启动前成功完成，如果未成功完成，会pod会重启，直到initC成功，如果restartPolicy为never，则pod不会重启



MainC 退出，则容器结束

###### 探针

由kubelet调用容器实现的Handler对容器执行定期的诊断

| 探针            |                                                              |
| --------------- | ------------------------------------------------------------ |
| ExecAction      | 在容器内执行指定命令，命令退出返回状态码0则认为诊断成功      |
| TCPSocketAction | 对指定端口的容器IP地址进行TCP检查，如果端口打开，则诊断成功  |
| HTTPGetAction   | 对指定的端口和路劲上的容器IP地址进行HTTP Get请求，返回状态码大于等于200且小于400 则诊断认为成功 |

探测方案：

livenessProbe：存活监测   指示容器是否正在运行，如果存活探测失败，则kubelet会杀死容器，并且容器受重启策略，如果容器不提供存活探针，则默认状态为Success

readinessProbe：就绪监测  指示容器是否准备好服务请求，如果就绪探测失败，端点控制器将从与pod匹配的所有service的端点删除该pod的IP地址；初始延迟之前的就绪状态默认为Failure，如果不提供就绪探针，默认状态为Success

#### 资源控制器

##### ReplicationController和ReplicaSet

RC用来确保容器应用的副本数始终保持在用户自定义的副本，如果容器有异常退出，会自动创建新的Pod替代，异常多出来也会自动回收，新版本中使用RelicaSet代替RC  二者无本质区别

##### Deployment

为Pod和RelicaSet提供一个声明式方法，替代以前的RC，典型应用场景包括：

定义一个Deployment来创建Pod和RelicaSet

滚动式升级和回滚式应用

例如：控制器：nginx-deployment

```
回滚服务:kubectl rollout undo deployment/nginx-deployment
检查升级历史： kubectl rollout history deployment/nginx-deployment
回退到指定版本：kubectl rollout undo deployment/nginx-deployment --to-revision=2
```

```
查看滚动升级状态:kubectl rollout status deployment/nginx-deployment
暂停更新：kubectl rollout pause deployment/nginx-deployment
更新镜像:kubectl set image deployment/nginx-deployment nginx=nginx:1.9.1
```

扩容与缩容 ：

kubectl scale deployment nginx-deployment --replicas 10

```
设置自动扩展：
kubectl autoscale deployment nginx-deployment --min=10 --max=15 --cpu-percent=80
```

暂停和继续Deployment

声明式编程：apply

命令式（rs）：create

------

##### DaemonSet ：

守护Pod 确保全部或者部分Node上运行一个Pod副本，当有新Node加入集群，会为他们新增一个Pod，当有Node从集群中移除，响应的Pod会被移除，应用场景：

运行集群存储daemon,在每个Node上运行glusterd，ceph

在每个Node上运行日志收集daemon，如logstash

在每个Node上运行监控daemon

Job：负责批量处理任务，仅仅执行一次任务，保证批量处理任务一个或者多个Pod成功结束

##### CronJob

管理基于Job，即在给定的时间运行一次，周期性的运行，发送邮件 定时重启

StatefulSet作为Crontroller为Pod提供唯一的标识，可以保证部署和scale顺序，statefulSet解决有状态服务问题，应用场景：

稳定的持久化存储，pod重启

稳定的网络标识，即pod重启后的podname和虚拟IP地址不变

有序部署，有序扩展，pod依次进行，在下一个pod运行前，之前的pod必须是running或者ready状态

有序收缩，有序删除

------

#####  Service

| 端口类型   | 作用                                                         |
| ---------- | ------------------------------------------------------------ |
| port       | k8s集群访问service的端口，通过clusterIP：port即可访问到该service |
| nodePort   | 外部机器可以访问的端口，外部机器可直接访问到service          |
| targetPort | pod容器的端口，从port或nodePort的流量最后经过kube-roxy流入到后端pod的targetPod上，最后访问到容器 |

简称svc，通过Label Selector映射到相应的deployment或rc，svc仅有一个负载策略，RB，只能基于IP地址或者端口实现转发请求，不支持主机名或者域名实现负载均衡与转发

ClusterIp：默认类型，自动分配一个Cluster内部可以访问的虚拟IP

NodePort：基于ClusterIp类型，在node上开一个端口，将该端口的流量导入到kube-proxy，然后由kube-proxy根据轮询规则，找到对应的pod，通过NodeIp：NodePort来访问

LoadBalancer：在NodePort的基础上，借助云供应商，创建一个外部负载均衡器，将请求转发到NodeIp：NodePort上

ExternalName：把集群外部服务引入到集群内部使用，没有任何代理被创建；通过返回的CNAME和它的值，可以将服务映射到externalName字段的内容，externalName类型没有selector特没有任何特定的端口和Endpoint，仅通过返回外部服务的别名来提供服务33

service代理模式分类：

userspace：所有服务经过kube-proxy，

iptables：

ipvs：所有调度规则，将流量重定向到后端的pod中

##### ingress







#### kubeadm

初始化集群

生成永久token  kubeadm token create --ttl 0

#### kubelet

运行集群上所有的节点，负责启动pod和容器

#### kubectl

Kubernetes命令行工具，部署和管理应用，查看各种组件

命令 :kubectl [command] [type] [name] [flags]

type:指定资源类型

name：指定资源类型的名字，区分大小写

##### 相关操作解读

| 操作                                             | 命令                                                         | 描述                                                         |
| :----------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| [annotate](https://www.kubernetes.org.cn/doc-46) | kubectl annotate (-f FILENAME \| TYPE NAME \| TYPE/NAME) KEY_1=VAL_1 ... KEY_N=VAL_N [--overwrite] [--all] [--resource-version=version] [flags] | 为一个或多个资源添加注释                                     |
| api-versions                                     | kubectl api-versions [flags]                                 | 列出支持的API版本。                                          |
| apply                                            | kubectl apply -f FILENAME [flags]                            | 对文件或stdin的资源进行配置更改。                            |
| attach                                           | kubectl attach POD -c CONTAINER [-i] [-t] [flags]            | 连接到一个运行的容器，既可以查看output stream，也可以与容器(stdin)进行交互。 |
| autoscale                                        | kubectl autoscale (-f FILENAME \| TYPE NAME \| TYPE/NAME) [--min=MINPODS] --max=MAXPODS [--cpu-percent=CPU] [flags] | 自动扩容/缩容由replication controller管理的一组pod。         |
| cluster-info                                     | kubectl cluster-info [flags]                                 | 显示有关集群中master和services的终端信息。                   |
| config                                           | kubectl config SUBCOMMAND [flags]                            | 修改kubeconfig文件。有关详细信息，请参阅各个子命令。         |
| create                                           | kubectl create -f FILENAME [flags]                           | 从file或stdin创建一个或多个资源。                            |
| delete                                           | kubectl delete (-f FILENAME \| TYPE [NAME \| /NAME \| -l label \| --all]) [flags] | 从file，stdin或指定label 选择器，names，resource选择器或resources中删除resources。 |
| describe                                         | kubectl describe (-f FILENAME \| TYPE [NAME_PREFIX \| /NAME \| -l label]) [flags] | 显示一个或多个resources的详细状态。                          |
| [edit](https://www.kubernetes.org.cn/doc-62)     | kubectl edit (-f FILENAME \| TYPE NAME \| TYPE/NAME) [flags] | 使用默认编辑器编辑和更新服务器上一个或多个定义的资源。       |
| exec                                             | kubectl exec POD [-c CONTAINER] [-i] [-t] [flags] [-- COMMAND [args...]] | 对pod中的容器执行命令。                                      |
| explain                                          | kubectl explain [--include-extended-apis=true] [--recursive=false] [flags] | 获取各种资源的文档。例如pod，node，services等                |
| expose                                           | kubectl expose (-f FILENAME \| TYPE NAME \| TYPE/NAME) [--port=port] [--protocol=TCP\|UDP] [--target-port=number-or-name] [--name=name] [----external-ip=external-ip-of-service] [--type=type] [flags] | 将 replication controller，service或pod作为一个新的Kubernetes service显示。 |
| get                                              | kubectl get (-f FILENAME \| TYPE [NAME \| /NAME \| -l label]) [--watch] [--sort-by=FIELD] [[-o \| --output]=OUTPUT_FORMAT] [flags] | 列出一个或多个资源。                                         |
| label                                            | kubectl label (-f FILENAME \| TYPE NAME \| TYPE/NAME) KEY_1=VAL_1 ... KEY_N=VAL_N [--overwrite] [--all] [--resource-version=version] [flags] | 添加或更新一个或多个资源的flags。                            |
| logs                                             | kubectl logs POD [-c CONTAINER] [--follow] [flags]           | 在pod中打印容器的日志。                                      |
| patch                                            | kubectl patch (-f FILENAME \| TYPE NAME \| TYPE/NAME) --patch PATCH [flags] | 使用strategic merge 补丁程序更新资源的一个或多个字段。       |
| port-forward                                     | kubectl port-forward POD [LOCAL_PORT:]REMOTE_PORT [...[LOCAL_PORT_N:]REMOTE_PORT_N] [flags] | 将一个或多个本地端口转发到pod。                              |
| proxy                                            | kubectl proxy [--port=PORT] [--www=static-dir] [--www-prefix=prefix] [--api-prefix=prefix] [flags] | 在Kubernetes API服务器运行代理。                             |
| replace                                          | kubectl replace -f FILENAME                                  | 从file或stdin替换资源，和edit操作类似 均可实现资源更新相关操作。 |
| rolling-update                                   | kubectl rolling-update OLD_CONTROLLER_NAME ([NEW_CONTROLLER_NAME] --image=NEW_CONTAINER_IMAGE \| -f NEW_CONTROLLER_SPEC) [flags] | 通过逐步替换指定的replication controller及其pod来执行滚动更新。 |
| run                                              | kubectl run NAME --image=image [--env="key=value"] [--port=port] [--replicas=replicas] [--dry-run=bool] [--overrides=inline-json] [flags] | 在集群上运行指定的镜像。                                     |
| scale                                            | kubectl scale (-f FILENAME \| TYPE NAME \| TYPE/NAME) --replicas=COUNT [--resource-version=version] [--current-replicas=count] [flags] | 更新指定replication controller的大小。                       |
| version                                          | kubectl version [--client] [flags]                           | 显示客户端和服务器上运行的Kubernetes版本。                   |

##### 资源类型

##### 输出选项

格式：kubectl [command] [TYPE] [NAME] -o=<output_format>

| 输出格式                          | 描述                                                         |
| :-------------------------------- | :----------------------------------------------------------- |
| -o=custom-columns=<spec>          | 使用逗号分隔的[custom columns](https://kubernetes.io/docs/user-guide/kubectl-overview/#custom-columns)列表打印一个表。 |
| -o=custom-columns-file=<filename> | 使用文件中的[custom columns](https://kubernetes.io/docs/user-guide/kubectl-overview/#custom-columns)模板打印表<filename>。 |
| -o=json                           | 输出JSON格式的API对象。                                      |
| -o=jsonpath=<template>            | 打印在[jsonpath](https://kubernetes.io/docs/user-guide/jsonpath)表达式中定义的字段。 |
| -o=jsonpath-file=<filename>       | 打印由 file中的[jsonpath](https://kubernetes.io/docs/user-guide/jsonpath)表达式定义的字段<filename>。 |
| -o=name                           | 仅打印资源名称，而不打印其他内容。                           |
| -o=wide                           | 以纯文本格式输出任何附加信息。对于pod，包括node名称。        |
| -o=yaml                           | 输出YAML格式的API对象。                                      |



#### etcd

可信赖的分布式减值存储服务，为整个集群提供关键数据。协助分布式集群正常运转

#### apiserver

所有服务统一入口

#### CrontrollerManager

维持副本期望数

#### Scheduler

负责介绍任务，选择合适的节点进行分配任务

#### Flannel

为k8s集群提供网络服务

kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/a70459be0084506e4ec919aa1c114638878db11b/Documentation/kube-flannel.yml 





### Pod

同一个Pod内部通讯，共享一个网络命名空间

不同Pod通信，



| 分类            | 特点                                      |      |
| --------------- | ----------------------------------------- | ---- |
| 自助式Pod       |                                           |      |
| 控制器管理的Pod | 如果容器异常退出，会自动创建新的Pod代替， |      |



### 安装K8S单节点

1、配置k8s的yum源

```
[kubernetes]
name=Kubernetes
baseurl=http:``//mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=http:``//mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg http://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
exclude=kube*
```

2 关闭selinux设置

3、修改内核参数sysctl.conf文件

```
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
```

sysctl  --system

4 关闭swap，并且在/etc/fstab内注释swap配置

swapoff -a

5、安装kubelet kubeadm 和kubectl

yum install -y  kubelet kubeadm  kubectl   --disableexcludes=kubernetes

systemctl enable kubelet && systemctl start kubelet

### k8s单节点搭建

#### 配置yum源

wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo 

 yum makecache 

#### 安装etcd和Kubernetes软件

yum install -y etcd kubernetes



修改/etc/sysconfig/docker

$ vim /etc/sysconfig/docker

 OPTIONS='--selinux-enabled=false --insecure-registry gcr.io'



Kubernetes修改apiserver的配置文件，在/etc/kubernetes/apiserver中

vim /etc/kubernetes/apiserver KUBE_ADMISSION_CONTROL="--admission_control=NamespaceLifecycle,NamespaceExists, LimitRanger,SecurityContextDeny,ServiceAccount,ResourceQuota"

按顺序启动以下服务：

systemctl start etcd systemctl start docker systemctl start kube-apiserver.service systemctl start kube-controller-manager.service systemctl start kube-scheduler.service systemctl start kubelet.service systemctl start kube-proxy.service

### 集群搭建（k8s 1.15版本）

官方文档：https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/

安装master节点初始化，在集群中，所有节点都要安装kubelet kubeadm 和kubectl

准备：

配置host文件：vim /etc/hosts

IP地址：master

IP地址：node1

IP地址：node2

关闭防火墙和禁用swap：

1、swapoff -all

2、配置fstab文件，注释swap配置

配置iptable请求：vi /etc/sysctl.conf

net.bridge.bridge-nf-call-ip6tables = 1 

net.bridge.bridge-nf-call-iptables = 1 

#### 安装指定docker

wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo -O /etc/yum.repos.d/docker-ce.repo
yum -y install docker-ce-18.06.1.ce-3.el7
systemctl enable docker && systemctl start docker
docker --version
 cat  > /etc/docker/daemon.json  <<EOF
{
  "registry-mirrors": ["https://yywkvob3.mirror.aliyuncs.com"],
  "exec-opts": ["native.cgroupdriver=systemd"]
}
EOF



#### 安装kubeadm组件：

cat > /etc/yum.repos.d/kubernetes.repo << EOF
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
yum install -y kubelet-1.15.0 kubeadm-1.15.0 kubectl-1.15.0
systemctl enable kubelet

#### 集群master初始化

kubeadm init \
  --apiserver-advertise-address=192.168.56.190 \
  --image-repository registry.aliyuncs.com/google_containers \
  --kubernetes-version v1.15.0 \
  --service-cidr=10.1.0.0/16 \
  --pod-network-cidr=10.244.0.0/16

mkdir -p $HOME/.kube 

cp -i /etc/kubernetes/admin.conf $HOME/.kube/config 

chown $(id -u):$(id -g) $HOME/.kube/config

将master的admin.conf 文件拷贝到node节点$HOME/.kube/目录下，并改名：config

#### node节点加入集群：

kubeadm join 192.168.56.190:6443 --token yxasby.0965o9ey5cvkhsx2 \
    --discovery-token-ca-cert-hash sha256:8f14a02842632eb081c9bff98c843ef4cafe27f26a71fa897cf02f1fbce2bfba

#### 部署flannel

kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/a70459be0084506e4ec919aa1c114638878db11b/Documentation/kube-flannel.yml 

检查节点pod状态：

 `kubectl get pod -n kube-system -o wide`

检查node状态为ready即可

kubectl get node -o wide

```
kubectl apply -f https:``//raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

### 搭建dashboard

wget https://raw.githubusercontent.com/kubernetes/dashboard/v1.5.1/src/deploy/kubernetes-dashboard.yaml
#修改image: registry.cn-hangzhou.aliyuncs.com/google_containers/kubernetes-dashboard-amd64:v1.10.0

#### 应用配置

kubectl create -f kubernetes-dashboard.yaml
#[root@docker ui]# kubectl get pod -A -o wide |grep dash
#kube-system   kubernetes-dashboard-7d46676dcb-2zrs7   1/1     Running   0          10m     10.244.1.9       docker    <none>           <none>
#[root@docker ~]# kubectl get svc -A -o wide |grep dash
#kube-system   kubernetes-dashboard   NodePort    10.1.39.194    <none>        443:30389/TCP            6h24m   k8s-app=kubernetes-dashboard

#### 创建登陆账户

kubectl create serviceaccount dashboard-admin -n kube-system
kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=kube-system:dashboard-admin

#### 浏览器访问

 https://IP:30389, 输入登陆密钥：
kubectl describe secrets -n kube-system $(kubectl -n kube-system get secret | awk '/dashboard-admin/{print $1}')
