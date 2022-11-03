## docker搭建私有仓库

### 拉取docker  私有镜像仓库

docker  pull  registry

### 启动仓库镜像

docker run  -d -p 5000：5000  --restart=always  --name=private-docker-registry   --privileged=true -v /home/registry:/var/lib/registry   镜像ID

–privileged=true”使容器真正具有容器内的root权限

/var/lib/registry”是私有仓库容器存放镜像的目录

### 修改镜像标签：

docker  tag  镜像:版本    ip地址：端口/镜像:版本

### 推送镜像到仓库

docker  push  p地址：端口/镜像:版本

失败原因：

docker默认使用https安全模式访问和操作，在这里我们使用普通的http模式

```
#vi /etc/docker/daemon.json{
    "insecure-registries": ["<ip>:5000"] 
}

安全模式：

{
    "registry-mirrors": ["<ip>:5000"] 
}
```

### 仓库设置用户权限：

mkdir  /home/auth

sh -c  "docker run --entrypoint htpasswd registry:latest -Bbn hello world > /home/auth/htpasswd"



用户：hello

密码：world