# k8s in progress

k8s的学习和测试仓库，里面堆满了有用没用的东西。

推荐去看一遍k8s in action。基础。

# 目录结构和作用解释

* install-k8s.md: [安装k8s](install-k8s.md)
* install-nfs.md: [安装nfs](install-nfs.md)
* install-registry.md: [安装registry](install-registry.md)
* calico: [calico CNI的安装，配置，和抓包](calico/README.md)。
* k8s.md: [k8s相关文档](k8s.md)
* minikube.md: [minikube相关文档](minikube.md)
* sched: [调度测试](sched/README.md)。
* deb: 基础镜像的定义。
  * apt: 里面放了两个基础文件，`proxy`和`sources.list`。允许动态升级系统。
  * apt-cm-create.sh: 使用apt目录生成对应configmap。
  * apt-cm.yaml: 所生成的configmap。
  * base-pod.yaml: 最基本的deb镜像定义的pod。
  * cm-pod.yaml: 使用configmap定义的pod，加载了动态升级功能。
* api: 目录内都是k8s api访问的例子。
  * ambassador.yaml: 两个containers，一个来自`luksa/kubectl-proxy`，一个是标准的debian。标准debian中，可使用curl访问本机8001端口，来访问k8s api而免去认证。具体参考`k8s in action`的`8.2.3`节。
  * curl-env.sh: 如何使用标准的curl来直接访问k8s api。
  * downward-pod.yaml: downward api的例子。
* nfs-subdir-external-provisioner: nfs-subdir-external-provisioner的部署文件。
  * kustomization.yaml: 按step 2和step 5要求创建的kustomize文件。
  * namespace.yaml: 按step 3要求创建的kustomize文件。
  * patch_nfs_details.yaml: 按step 4要求创建的kustomize文件。
  * 最后`kubectl kustomize`编译执行。
* vol: [卷挂载有关的部分](vol/README.md)
* kubia: `k8s in action`的示例资源
  * manual-pod.yaml: 手工创建的pod，具备基础功能。
  * rs.yaml: 标准replicaset。
  * deploy.yaml: 标准deployment。
  * svc.yaml: 标准service。
* myapp: [myapp相关资源](myapp/README.md)。myapp有版本无状态。
* mysrv: [mysrv相关资源](mysrv/README.md)。mysrv有状态无版本。
* sec-ctx: 安全隔离有关的文件。具体看`k8s in action`第十三章。
  * file-pod.yaml: 容器内访问主机文件。
  * net-pod.yaml: 容器内访问主机网络（hostNetwork）。
  * pid-pod.yaml: 容器内访问主机PID空间。（ps可见列表）
  * priv-pod.yaml: 容器内拥有特权。

# Kubernetes Metrics Server

metric server。部署后top开始工作，可以使用hpa。

具体看[Kubernetes Metrics Server](https://github.com/kubernetes-sigs/metrics-server)。
