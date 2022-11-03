服务于端口

| 软件                    | 端口      | 协议 | 用途                         |
| ----------------------- | --------- | ---- | ---------------------------- |
| kube-apiserver          | 6443      | TCP  | 组件接口服务                 |
| etcd                    | 2379-2380 | TCP  | kube-api  etcd服务           |
| kubelet                 | 10250     | TCP  | kubelet服务                  |
| kube-scheduler          | 10251     | TCP  | kube-scheduler服务           |
| kube-controller-manager | 10252     | TCP  | kube-controller-manager 服务 |

