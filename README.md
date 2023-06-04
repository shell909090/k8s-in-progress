# k8s in progress

k8s的学习和测试仓库，里面堆满了有用没用的东西。

推荐去看一遍k8s in action。基础。

# 目录结构和作用解释

* doc: 文档有关
  * install-k8s.md: [安装k8s](doc/install-k8s.md)
  * install-registry.md: [安装registry](doc/install-registry.md)
  * k8s.md: [k8s相关文档](doc/k8s.md)
  * k8s-in-minimum.md: [最小化的k8s](doc/k8s-in-minimum.md)
  * node-failure.md: [node失效和迁移测试](doc/node-failure.md)
  * minikube.md: [minikube相关文档](doc/minikube.md)
* calico: [calico CNI的安装，配置，和抓包](calico/)
* base: [基础镜像有关的东西](base/)
* api: [k8s api有关的东西](api/)
* nfs: [nfs有关的部分](nfs/)
* vol: [卷挂载有关的部分](vol/)
* kubia: [k8s in action的示例资源](kubia/)
* myapp: [myapp相关资源](myapp/)。myapp有版本无状态。
* mysrv: [mysrv相关资源](mysrv/)。mysrv有状态无版本。
* sched: [调度测试](sched/)
* sec-ctx: [安全隔离有关的文件](sec-ctx/)
* demo: [示例性项目](demo/)
* ingress: [两个ingress配置](ingress/)
