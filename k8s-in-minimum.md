# 最小化的k8s

用最短的篇幅，介绍k8s里的核心概念。原则是，如果去除一个概念不影响完成一个最小化的项目，那就跳过这个概念。

## 什么是k8s

k8s核心是一套分布式supervisor，保证应用在多台机器上的执行，关闭，互相访问。

# 容器

简单来说，容器是一种隔离空间。在容器里运行的一切和宿主以及其他容器隔离。

## 容器运行时

原理上说，k8s可以配合多种底层。实际上，k8s底层（目前）只支持一种东西，CRI(Container Runtime Interface)。CRI定义了一系列接口。理论上k8s可以搭配一切支持CRI的虚拟化系统使用。但实际中官方主要列出了以下四种支持：

* containerd
* crio
* docker
* mirantis

同时，lxc也提供了CRI支持。[1]

引用：

1. [lxcri](https://github.com/lxc/lxcri)

# 对象

## node

node对象是主机的体现。一个kubelet配合一个容器运行时就可以注册为一个node。

有趣的是，如果同一台机器上跑了两种不同的运行时，各自配置了一个kubelet实例，会变成几个node？

我猜是两个。

## pod

pod对象是容器的集合，里面可以有一到多个容器。这些容器在同一台机器上，共享相同的命名空间。

技术上说，这基于两方面的因素。一方面因为系统虚拟化容器在同一个容器内运行多个程序的要求。但用过kubectl exec的朋友就应该知道，同一个容器内是可以运行多个进程的。这个功能在基于vm的容器和系统虚拟化容器上都可以实现。另一方面，系统虚拟化容器给了我们一个便利，在同一个容器上运行的两个程序可以很方便的拥有两套根文件系统。基于vm的容器想做到这点就只有chroot了。

结合上面两点后，我们很容易做到很多有趣的事情。例如辅助调试的sidecar容器。第二容器可以在完全不同的镜像上执行，并有全套调试工具。同一空间允许调试工具方便的探测运行中进程，以及执行各种操作。同时，这丝毫不破坏主容器的最小化配置。

## svc

svc描述一组条件。访问svc里指定的IP:port时，应当被路由到符合svc描述条件的pod上去。

# 组件

## etcd

一个分布式强一致性kv存储。k8s使用etcd保存其核心配置。

大概相当于Windows的注册表。

## kube-apiserver

apiserver是对etcd的一层包装。理论上所有组件应当只和apiserver通信，而不需要知道etcd的存在。

apiserver的所有client都可以关注一个或多个对象，在对象被更新时得到通知。

使用apiserver隔离有助于解决鉴权问题（当然，不止于此）。

## kubelet

kubelet接受两类输入，和容器运行时通讯，管理容器运行。

* manifest文件: 在没有外部指定的情况下，可以使用预先定义好的manifest文件来启动容器。这主要是为了解决自举时apiserver和kubelet哪个先启动的问题。
* apiserver: kubelet向特定apiserver注册，此过程会产生或更新node对象。同时，kubelet关注所有pod对象的更新。一旦归属于本node的pod更新了，kubelet就启动或关闭容器。但是kubelet丝毫不关心pod的建立，归属于什么node之类的问题。

## kube-scheduler

scheduler只关注pod和node对象。scheduler负责将pod绑定到特定的node。

scheduler不关注pod和node为何被创建和凋亡。

## kube-controller-manager

controller可以说是k8s的核心。其主要功能就是关注一类或多类对象。在状态发生变化时，调整其他对象的属性来进行配合。

例如，在deploy属性发生变更时，创建新的pod，并干掉老的pod。持续上述操作，直到所有pod都应用新版属性。

controller并不关心创建出来的pod对象如何被调度和执行。

## kube-proxy

kube-proxy用于支撑svc。它保证所有和特定IP:port的通讯都会被路由到正确的后端。

kube-proxy需要执行在每个节点上。但它并不需要特意被执行。kube-proxy被定义为具备特权的ds对象。kube-controller-manager会为每个node创建一个pod。随后对应节点的kubelet会负责启动一个包含了对应程序的pod。

## kube-dns/CoreDNS

这两个组件达成同一个目地——将对特定name.namespace的访问，转换成pod对应的真实IP。

原来是kube-dns，新版本中被CoreDNS替换。

# 网络

网络是k8s最复杂的部分，因为k8s自身并没有完整的网络实现。k8s的网络是依靠网络插件来实现的。

无论何种网络插件，基本的要求（不考虑network policy的话）是一致的。

* 所有的pod均可互相访问
* pod保证可以访问到node，node不保证可以访问到pod

一般设计，会给pod和node独立的网络地址空间。同时，由于pod间会跨网络访问，因此网络系统必须能解决诸如某个IP对应哪个node之类的问题。为了减少这类问题的复杂度，一般会给同一台node上的pod同一个网段的地址，以便路由收敛。

# 过程分析

## k8s启动过程

k8s的启动中，只有一个组件是需要系统来启动的——kubelet。

在master的kubelet启动后，minifest文件会（默认）要求启动四个pod。

* etcd
* kube-apiserver
* kube-controller-manager
* kube-scheduler

随后就会产生一个，只有一个（或一组）master的集群。

而后启动一个node，上面的kubelet就会启动并加入集群。集群里定义了应该启动什么（例如kube-proxy）。kubelet就会照着执行。

## 服务启动和调度过程

我们以一个最简单的服务，来描述整个启动和调度的过程。这个服务包含以下两个对象。

* deployment对象
* service对象

在deployment对象被创建后，依次发生了以下过程。

1. kube-controller-manager负责解析deploy对象，创建rs对象。
2. kube-controller-manager负责解析rs对象，负责创建pod对象。
3. kube-scheduler负责调度pod，将pod绑定到特定node。
4. node上的kubelet负责将容器创建出来。

在service对象被创建后，依次发生了以下过程。

1. kube-proxy更新路由机制。
2. kube-dns负责更新DNS数据，保证svcname.domain可以访问到正确的IP。

# 其他可能有帮助的对象

* deployment: 一个deploy会启动一组多个pod，每个pod都是无状态的，可以独立提供服务。
* statefulset: 一个sts会启动一组pod，不同的是每个pod都是有状态的。
* daemonset: 一个ds会在每一台机器上启动一个pod。一般这个pod会获得某方面的特权，来提供一定的，节点上必须的服务。
* cronjob/job: 在特定的时候启动一个pod。

# 如何创建一个最小化的k8s

注意，我说的是原版k8s，不是minikube或者k8s。

开一个node。把taint干掉。

完了。
