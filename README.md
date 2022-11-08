# k8s in progress

k8s的学习和测试仓库，里面堆满了有用没用的东西。

推荐去看一遍k8s in action。基础。

# 目录结构和作用解释

* doc: 文档有关
  * install-k8s.md: [安装k8s](doc/install-k8s.md)
  * install-registry.md: [安装registry](doc/install-registry.md)
  * k8s.md: [k8s相关文档](doc/k8s.md)
  * k8s-in-minimum.md: [最小化的k8s](doc/k8s-in-minimum.md)
  * minikube.md: [minikube相关文档](doc/minikube.md)
* calico: [calico CNI的安装，配置，和抓包](calico/README.md)。
* sched: [调度测试](sched/README.md)。
* deb: [基础镜像有关的东西](deb/)
* api: [k8s api有关的东西](api/)
* nfs: [nfs有关的部分](nfs/)
* vol: [卷挂载有关的部分](vol/)
* kubia: [k8s in action的示例资源](kubia/)
* myapp: [myapp相关资源](myapp/)。myapp有版本无状态。
* mysrv: [mysrv相关资源](mysrv/)。mysrv有状态无版本。
* sec-ctx: [安全隔离有关的文件](sec-ctx/)。

# Kubernetes Metrics Server

metric server。部署后top开始工作，可以使用hpa。

具体看[Kubernetes Metrics Server](https://github.com/kubernetes-sigs/metrics-server)。
