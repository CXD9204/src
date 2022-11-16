参考文档1:http://docs.kubernetes.org.cn/468.html

参考文档2:https://linfan1.gitbooks.io/kubernetes-chinese-docs/content/150-kubectl_exec.html

LoadBalancer Service Inpress的区别

deployment,Replication Controller 与Replicasets 的区别



![image-20221110103917280](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20221110103917280.png)

### kubectl cp

容器与本地宿主机文件互传赋值

```
kubectl cp file1 容器:/<dir>
```

### kubectl annotate

更新一个或多个资源的Annotations信息  如果同一个annotation多次设置，则只使用最后设置的value值。

如果--overwrite为true，现有的annotations可以被覆盖，否则试图覆盖annotations将会报错。

如果设置了--resource-version，则更新将使用此resource version，否则将使用原有的resource version。

```
设置annotation “description”的value “my frontend”
kubectl annotate pods foo description='my frontend'

设置annotation“description”的value“my frontend running nginx”，覆盖现有的值。
kubectl annotate --overwrite pods foo description='my frontend running nginx'

```



### kubectl run

创建并运行一个或多个容器镜像或者创建一个deployment 或job 来管理容器

```shell
kubectl run nginx --image=nginx

启动nginx实例，设置副本数5
kubectl run nginx --image=nginx --replicas=5

kubectl run nginx  --image=nginx --port=8080 --replicas=5
```

### kubectl scale

扩容或缩容 Deployment、ReplicaSet、Replication Controller或 Job 中Pod数量

```
名为foo中的pod副本数设置为3
kubectl scale --replicas=3 rs/foo
```

### kubectl autoscale

自动设置Deployment、ReplicaSet或ReplicationController在kubernetes集群中运行的pod数量（水平自动伸缩）

```
使用 Deployment “foo”设定，使用默认的自动伸缩策略，指定目标CPU使用率，使其Pod数量在2到10之间。
kubectl autoscale deployment foo --min=2 --max=10

使用RC“foo”设定，使其Pod的数量介于1和5之间，CPU使用率维持在80％。
kubectl autoscale rc foo --max=5 --cpu-percent=80

```

### kubectl get

获取列出一个或多个资源的信息。

```
列出Pod以及运行Pod节点信息。
kubectl get pods|serice|replicationcontroller |... -o wide
```

### kubectl label

label 必须以字母或数字开头，可以使用字母、数字、连字符、点和下划线，最长63个字符。

如果--overwrite 为 true，则可以覆盖已有的 label，否则尝试覆盖 label 将会报错

如果指定了--resource-version，则更新将使用此资源版本，否则将使用现有的资源版本。

```
给名为foo的Pod添加label unhealthy=true。
kubectl label pods foo unhealthy=true
```



### kubectl logs

查看日志信息

kubectl  logs  -f  pod_name

```
持续输出日志
kubectl  logs  -f  nginx

返回pod ruby中已经停止的容器web-1的日志快照
$ kubectl logs -p -c ruby web-1
```

### kubectl exec

连接容器并执行操作

```
kubectl exec -it pod_name -- bash
# 默认在nginx容器中运行“ls”并获取输出,-c 容器名  -p pod名
kubectl exec pod nginx ls

```

### kubectl delete

通过配置文件名、stdin、资源名称或label选择器来删除资源, 要强制删除资源，需指定- force flag，且设置周期（宽限期）为0

```
删除名为“baz”和“foo”的Pod和Service。
kubectl delete pod,service baz foo

强制删除dead node上的pod
kubectl delete pod foo --grace-period=0 --force

```

### kubectl rollout history

查看之前的推出版本

```
$ history (TYPE NAME | TYPE/NAME) [flags]
查看deployment的历史记录
kubectl rollout history deployment/abc

```

### kubectl rollout undo

回滚历史版本

```
undo (TYPE NAME | TYPE/NAME) [flags]
回滚到最近的某一个deployment版本
kubectl rollout undo deployment/abc

回滚到daemonset 修订3版本
kubectl rollout undo daemonset/abc --to-revision=3


```

## Kubectl 上下文和配置

设置 kubectl 与其通信的 Kubernetes 集群，以及修改配置信息。请参阅 [使用 kubeconfig 跨集群进行身份验证](http://docs.kubernetes.org.cn/823.html) 文档获取详细的配置文件信息。

```
$ kubectl config view # 显示合并的 kubeconfig 设置。

# 同时使用多个 kubeconfig 文件，并且查看合并的配置
$ KUBECONFIG=~/.kube/config:~/.kube/kubconfig2 kubectl config view

# 查看名称为 “e2e” 的用户的密码
$ kubectl config view -o jsonpath='{.users[?(@.name == "e2e")].user.password}'

$ kubectl config current-context              # 显示当前上下文
$ kubectl config use-context my-cluster-name  # 设置默认的上下文为 my-cluster-name

# 在 kubeconf 中添加一个支持基本鉴权的新集群。
$ kubectl config set-credentials kubeuser/foo.kubernetes.com --username=kubeuser --password=kubepassword

# 使用特定的用户名和命名空间设置上下文。
$ kubectl config set-context gce --user=cluster-admin --namespace=foo \
  && kubectl config use-context gce
```

## 创建对象

Kubernetes 清单可以用 json 或 yaml 来定义。使用的文件扩展名包括 .yaml, .yml 和 .json。

```
$ kubectl create -f ./my-manifest.yaml           # 创建资源
$ kubectl create -f ./my1.yaml -f ./my2.yaml     # 从多个文件创建资源
$ kubectl create -f ./dir                        # 通过目录下的所有清单文件创建资源
$ kubectl create -f https://git.io/vPieo         # 使用 url 获取清单创建资源
$ kubectl run nginx --image=nginx                # 开启一个 nginx 实例
$ kubectl explain pods,svc                       # 获取 pod 和服务清单的描述文档

# 通过标准输入创建多个 YAML 对象
$ cat <<EOF | kubectl create -f -
apiVersion: v1
kind: Pod
metadata:
  name: busybox-sleep
spec:
  containers:
  - name: busybox
    image: busybox
    args:
    - sleep
    - "1000000"
---
apiVersion: v1
kind: Pod
metadata:
  name: busybox-sleep-less
spec:
  containers:
  - name: busybox
    image: busybox
    args:
    - sleep
    - "1000"
EOF

# 使用多个 key 创建一个 secret
$ cat <<EOF | kubectl create -f -
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  password: $(echo -n "s33msi4" | base64)
  username: $(echo -n "jane" | base64)
EOF
```

## 查看、查找资源

```
# 具有基本输出的 get 命令
$ kubectl get services                          # 列出命名空间下的所有 service
$ kubectl get pods --all-namespaces             # 列出所有命名空间下的 pod
$ kubectl get pods -o wide                      # 列出命名空间下所有 pod，带有更详细的信息
$ kubectl get deployment my-dep                 # 列出特定的 deployment
$ kubectl get pods --include-uninitialized      # 列出命名空间下所有的 pod，包括未初始化的对象

# 有详细输出的 describe 命令
$ kubectl describe nodes my-node
$ kubectl describe pods my-pod

$ kubectl get services --sort-by=.metadata.name # List Services Sorted by Name

# 根据重启次数排序，列出所有 pod
$ kubectl get pods --sort-by='.status.containerStatuses[0].restartCount'

# 查询带有标签 app=cassandra 的所有 pod，获取它们的 version 标签值
$ kubectl get pods --selector=app=cassandra rc -o \
  jsonpath='{.items[*].metadata.labels.version}'

# 获取命名空间下所有运行中的 pod
$ kubectl get pods --field-selector=status.phase=Running

# 所有所有节点的 ExternalIP
$ kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="ExternalIP")].address}'

# 列出输出特定 RC 的所有 pod 的名称
# "jq" 命令对那些 jsonpath 看来太复杂的转换非常有用，可以在这找到：https://stedolan.github.io/jq/
$ sel=${$(kubectl get rc my-rc --output=json | jq -j '.spec.selector | to_entries | .[] | "\(.key)=\(.value),"')%?}
$ echo $(kubectl get pods --selector=$sel --output=jsonpath={.items..metadata.name})

# 检查那些节点已经 ready
$ JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}' \
 && kubectl get nodes -o jsonpath="$JSONPATH" | grep "Ready=True"

# 列出某个 pod 目前在用的所有 Secret
$ kubectl get pods -o json | jq '.items[].spec.containers[].env[]?.valueFrom.secretKeyRef.name' | grep -v null | sort | uniq

# 列出通过 timestamp 排序的所有 Event
$ kubectl get events --sort-by=.metadata.creationTimestamp
```

## 更新资源

```
$ kubectl rolling-update frontend-v1 -f frontend-v2.json           # 滚动更新 pod：frontend-v1
$ kubectl rolling-update frontend-v1 frontend-v2 --image=image:v2  # 变更资源的名称并更新镜像
$ kubectl rolling-update frontend --image=image:v2                 # 更新 pod 的镜像
$ kubectl rolling-update frontend-v1 frontend-v2 --rollback        # 中止进行中的过程
$ cat pod.json | kubectl replace -f -                              # 根据传入标准输入的 JSON 替换一个 pod

# 强制替换，先删除，然后再重建资源。会导致服务中断。
$ kubectl replace --force -f ./pod.json

# 为副本控制器（rc）创建服务，它开放 80 端口，并连接到容器的 8080 端口
$ kubectl expose rc nginx --port=80 --target-port=8000

# 更新单容器的 pod，将其镜像版本（tag）更新到 v4
$ kubectl get pod mypod -o yaml | sed 's/\(image: myimage\):.*$/\1:v4/' | kubectl replace -f -

$ kubectl label pods my-pod new-label=awesome                      # 增加标签
$ kubectl annotate pods my-pod icon-url=http://goo.gl/XXBTWq       # 增加注释
$ kubectl autoscale deployment foo --min=2 --max=10                # 将名称为 foo 的 deployment 设置为自动扩缩容
```

## 修补资源

```
$ kubectl patch node k8s-node-1 -p '{"spec":{"unschedulable":true}}' # 部分更新节点

# 更新容器的镜像，spec.containers[*].name 是必需的，因为它们是一个合并键
$ kubectl patch pod valid-pod -p '{"spec":{"containers":[{"name":"kubernetes-serve-hostname","image":"new image"}]}}'

# 使用带有数组位置信息的 json 修补程序更新容器镜像
$ kubectl patch pod valid-pod --type='json' -p='[{"op": "replace", "path": "/spec/containers/0/image", "value":"new image"}]'

# 使用带有数组位置信息的 json 修补程序禁用 deployment 的 livenessProbe
$ kubectl patch deployment valid-deployment  --type json   -p='[{"op": "remove", "path": "/spec/template/spec/containers/0/livenessProbe"}]'

# 增加新的元素到数组指定的位置中
$ kubectl patch sa default --type='json' -p='[{"op": "add", "path": "/secrets/1", "value": {"name": "whatever" } }]'
```

## 编辑资源

在编辑器中编辑任何 API 资源。

```
$ kubectl edit svc/docker-registry                      # 编辑名称为 docker-registry 的 service
$ KUBE_EDITOR="nano" kubectl edit svc/docker-registry   # 使用 alternative 编辑器
```

## 缩放资源

```
$ kubectl scale --replicas=3 rs/foo                                 # 缩放名称为 'foo' 的 replicaset，调整其副本数为 3
$ kubectl scale --replicas=3 -f foo.yaml                            # 缩放在 "foo.yaml" 中指定的资源，调整其副本数为 3
$ kubectl scale --current-replicas=2 --replicas=3 deployment/mysql  # 如果名称为 mysql 的 deployment 目前规模为 2，将其规模调整为 3
$ kubectl scale --replicas=5 rc/foo rc/bar rc/baz                   # 缩放多个副本控制器
```

## 删除资源

```
$ kubectl delete -f ./pod.json                                              # 使用 pod.json 中指定的类型和名称删除 pod
$ kubectl delete pod,service baz foo                                        # 删除名称为 "baz" 和 "foo" 的 pod 和 service
$ kubectl delete pods,services -l name=myLabel                              # 删除带有标签 name=myLabel 的 pod 和 service
$ kubectl delete pods,services -l name=myLabel --include-uninitialized      # 删除带有标签 name=myLabel 的 pod 和 service，包括未初始化的对象
$ kubectl -n my-ns delete po,svc --all                                      # 删除命名空间 my-ns 下所有的 pod 和 service，包括未初始化的对象
```

## 与运行中的 pod 交互

```
$ kubectl logs my-pod                                 # 转储 pod 日志到标准输出
$ kubectl logs my-pod -c my-container                 # 有多个容器的情况下，转储 pod 中容器的日志到标准输出
$ kubectl logs -f my-pod                              # pod 日志流向标准输出
$ kubectl logs -f my-pod -c my-container              # 有多个容器的情况下，pod 中容器的日志流到标准输出
$ kubectl run -i --tty busybox --image=busybox -- sh  # 使用交互的 shell 运行 pod
$ kubectl attach my-pod -i                            # 关联到运行中的容器
$ kubectl port-forward my-pod 5000:6000               # 在本地监听 5000 端口，然后转到 my-pod 的 6000 端口
$ kubectl exec my-pod -- ls /                         # 1 个容器的情况下，在已经存在的 pod 中运行命令
$ kubectl exec my-pod -c my-container -- ls /         # 多个容器的情况下，在已经存在的 pod 中运行命令
$ kubectl top pod POD_NAME --containers               # 显示 pod 及其容器的度量
```

## 与 node 和集群交互

```
$ kubectl cordon my-node                                                # 标记节点 my-node 为不可调度
$ kubectl drain my-node                                                 # 准备维护时，排除节点 my-node
$ kubectl uncordon my-node                                              # 标记节点 my-node 为可调度
$ kubectl top node my-node                                              # 显示给定节点的度量值
$ kubectl cluster-info                                                  # 显示 master 和 service 的地址
$ kubectl cluster-info dump                                             # 将集群的当前状态转储到标准输出
$ kubectl cluster-info dump --output-directory=/path/to/cluster-state   # 将集群的当前状态转储到目录 /path/to/cluster-state

# 如果带有该键和效果的污点已经存在，则将按指定的方式替换其值
$ kubectl taint nodes foo dedicated=special-user:NoSchedule
```

## 资源类型

下表列出了所有支持的资源类型及其缩写别名：

| Resource type              | Abbreviated alias |
| :------------------------- | :---------------- |
| all                        |                   |
| certificatesigningrequests | csr               |
| clusterrolebindings        |                   |
| clusterroles               |                   |
| componentstatuses          | cs                |
| configmaps                 | cm                |
| controllerrevisions        |                   |
| cronjobs                   |                   |
| customresourcedefinition   | crd               |
| daemonsets                 | ds                |
| deployments                | deploy            |
| endpoints                  | ep                |
| events                     | ev                |
| horizontalpodautoscalers   | hpa               |
| ingresses                  | ing               |
| jobs                       |                   |
| limitranges                | limits            |
| namespaces                 | ns                |
| networkpolicies            | netpol            |
| nodes                      | no                |
| persistentvolumeclaims     | pvc               |
| persistentvolumes          | pv                |
| poddisruptionbudgets       | pdb               |
| podpreset                  |                   |
| pods                       | po                |
| podsecuritypolicies        | psp               |
| podtemplates               |                   |
| replicasets                | rs                |
| replicationcontrollers     | rc                |
| resourcequotas             | quota             |
| rolebindings               |                   |
| roles                      |                   |
| secrets                    |                   |
| serviceaccount             | sa                |
| services                   | svc               |
| statefulsets               | sts               |
| storageclasses             | sc                |

## 输出格式

若要以特定格式将详细信息输出到终端窗口，可以将 -o 或者 -output 标志添加到支持它们的 kubectl 命令中。

| 输出格式                          | 描述                                                         |
| :-------------------------------- | :----------------------------------------------------------- |
| -o=custom-columns=<spec>          | 打印表，使用逗号分隔自定义列                                 |
| -o=custom-columns-file=<filename> | 打印表，使用 <filename> 文件中的自定义列模板                 |
| -o=json                           | 输出一个 JSON 格式的 API 对象                                |
| -o=jsonpath=<template>            | 打印由 [jsonpath](https://k8smeetup.github.io/docs/user-guide/jsonpath) 表达式定义的属性 |
| -o=jsonpath-file=<filename>       | 打印由文件 <filename> 中的 [jsonpath](https://k8smeetup.github.io/docs/user-guide/jsonpath) 表达式定义的属性 |
| -o=name                           | 仅打印资源名称                                               |
| -o=wide                           | 以纯文本格式输出，包含所有附加信息，对于 pod，则包括节点名称 |
| -o=yaml                           | 以 YAML 格式输出 API 对象                                    |

## kubectl 输出信息和调试

Kubectl 输出信息的详细程度由 -v 或者 --v 标志控制，后面跟着一个表示日志级别的整数。一般的 Kubernetes 日志记录约定以及相关日志级别描述在 [这里](https://github.com/kubernetes/community/blob/master/contributors/devel/logging.md)。

| 信息  | 描述                                                         |
| :---- | :----------------------------------------------------------- |
| --v=0 | 通常，这对操作者来说总是可见的。                             |
| --v=1 | 当您不想要很详细的输出时，这个是一个合理的默认日志级别。     |
| --v=2 | 有关服务和重要日志消息的有用稳定状态信息，这些信息可能与系统中的重大更改相关。这是大多数系统推荐的默认日志级别。 |
| --v=3 | 关于更改的扩展信息。                                         |
| --v=4 | 调试级别信息。                                               |
| --v=6 | 显示请求资源。                                               |
| --v=7 | 显示 HTTP 请求头。                                           |
| --v=8 | 显示 HTTP 请求内容。                                         |
| --v=9 | 显示 HTTP 请求内容，并且不截断内容                           |