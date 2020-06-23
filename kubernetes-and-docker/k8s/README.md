# Kubernetes (k8s)

### 目录

1. 开始使用 Kubernetes 和 Docker
    - 创建、 运行及共享容器镜像
    - 配置 Kubernetes 集群
    - 在 Kubernetes 上运行第一个应用
1. pod: 运行于 Kubernetes 中的容器
1. 副本机制和其他控制器：部署托管的 pod
1. 服务：让客户端发现 pod 并与之通信
1. 卷：将磁盘挂载到容器
1. ConfigMap 和 Secret : 配置应用程序
1. 从应用访问 pod 元数据以及其他资源
1. Deployment: 声明式地升级应用
1. StatefulSet : 部署有状态的多副本应用
1. 了解 Kubernetes 机理
    - 了解架构
    - 控制器如何协作
    - 了解运行中的 pod 是什么
    - 跨 pod 网络
    - 服务是如何实现的
    - 运行高可用集群
1. Kubernetes API 服务器的安全防护
1. 保障集群内节点和网络安全
1. 计算资源管理
1. 自动横向伸缩 pod 与集群节点
1. 高级调度
1. 开发应用的最佳实践
1. Kubernetes 应用扩展
    - 定义自定义 API 对象
    - 使用 Kubernetes 服务目录扩展 Kubernetes
    - 基于 Kubernetes 搭建的平台

### 附录

1. 在多个集群中使用 kubectl
1. 使用 kubeadm 配置多节点集群
1. 使用其他容器运行时
1. Cluster Federation（集群联邦）

—— 《Kubernetes in Action》


<br>

## 开始使用 Kubernetes 和 Docker （Quick Start）

### I Docker 环境搭建

#### 1.1 安装 Docker 并运行 Hello World 容器

``` bash
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update   #更新 apt 包索引
# 安装 apt 依赖包，通过 HTTPS 来获取仓库
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
# 添加 Docker 的官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key list                        #列出已保存在系统中的key
sudo apt-key fingerprint 0EBFCD88        #搜索指纹的后8个字符为0EBFCD88的密钥（确认docker的密钥存在）
# 设置稳定版仓库
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
# 安装 Docker Engine-Community
sudo apt-get update
# 安装 docker-ce 貌似就够了，docker-ce-cli 和 containerd.io 不装好像也能用
sudo apt-get install docker-ce docker-ce-cli containerd.io

# 测试 Docker 是否安装成功
sudo docker run hello-world
```

``` bash
sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io

# yum list docker-ce --showduplicates | sort -r
# sudo yum install docker-ce-<VERSION_STRING> docker-ce-cli-<VERSION_STRING> containerd.io

sudo systemctl start docker
sudo docker run hello-world
```

#### 1.2 创建一个简单的 Node.js 应用

#### 1.3 为镜像创建 Dockerfile

#### 1.4 构建容器镜像

#### 1.5 运行容器镜像

#### 1.6 探索运行容器的内部

#### 1.7 停止和删除容器

#### 1.8 向镜像仓库推送镜像


### II 配置 Kubernetes 集群


### III 在 Kubernetes 上运行第一个 Node.js 应用



## 2 pod: 运行于 Kubernetes 中的容器

