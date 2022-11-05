# k8s in progress

k8s的学习和测试仓库，里面堆满了有用没用的东西。

推荐去看一遍k8s in action。基础。

# 分目录作用解释

* install-k8s.md: [安装k8s](install-k8s.md)
* calico: calico CNI的安装，配置，和抓包。
  * calico.yaml: `wget https://docs.projectcalico.org/manifests/calico.yaml`
  * default-ipv4-ippool-bgp.yaml: bgp模式的配置，所有node需要在同一个大二层里。（或是网关bgp打通）
  * default-ipv4-ippool-ipip.yaml: ipip模式的配置，可以跨越网关。
  * default-ipv4-ippool-vxlan.yaml: vxlan模式的配置。同样进行封装，使用vxlan协议，而非ipip协议。
  * calico-*.pcap: 三种模式的抓包结果。
* deb: 基础镜像的定义
  * apt: 里面放了两个基础文件，`proxy`和`sources.list`。允许动态升级系统。
  * apt-cm-create.sh: 使用apt目录生成对应configmap。
  * apt-cm.yaml: 所生成的configmap。
  * base-pod.yaml: 最基本的deb镜像定义的pod。
  * cm-pod.yaml: 使用configmap定义的pod，加载了动态升级功能。
* api: 目录内都是k8s api访问的例子
  * ambassador.yaml: 两个containers，一个来自`luksa/kubectl-proxy`，一个是标准的debian。标准debian中，可使用curl访问本机8001端口，来访问k8s api而免去认证。具体参考`k8s in action`的`8.2.3`节。
  * curl-env.sh: 如何使用标准的curl来直接访问k8s api。
  * downward-pod.yaml: downward api的例子。
* nfs-subdir-external-provisioner: nfs-subdir-external-provisioner的部署文件。
  * kustomization.yaml: 按step 2和step 5要求创建的kustomize文件。
  * namespace.yaml: 按step 3要求创建的kustomize文件。
  * patch_nfs_details.yaml: 按step 4要求创建的kustomize文件。
  * 最后`kubectl kustomize`编译执行。
* vol: 卷挂载有关的部分
  * nfs-pvc.yaml: 基础pvc，创建了`nfs`，申请了10G存储。
  * nfs-pv.yaml: 基础pv，使用nfs作为底层存储。
  * nfs-subdir-pvc.yaml: pvc，创建里`nfs-subdir`, 使用`nfs-client`作为storage class，申请1G存储。
  * vol-git-pod.yaml: 使用`gitRepo`作为底层存储挂载。需要node上安装git。
  * vol-hostpath-pod.yaml: 使用`hostPath`作为底层存储。
  * vol-nfs-pod.yaml: 使用`nfs`作为底层存储。
  * vol-pvc-nfs-pod.yaml: 使用pvc `nfs`作为底层存储。
  * vol-pvc-nfs-subdir-pod.yaml: 使用pvc `nfs-subdir`作为底层存储。
* kubia: `k8s in action`的示例资源
  * manual-pod.yaml: 手工创建的pod，具备基础功能。
  * rs.yaml: 标准replicaset。
  * deploy.yaml: 标准deployment。
  * svc.yaml: 标准service。
* myapp: myapp相关资源。myapp有版本无状态。
  * Dockerfile-v1/Dockerfile-v2: dockerfile
  * Makefile: 编译文件。`make build_v1`编译第一个版本，`make build_v2`编译第二个。`push_v1`和`push_v2`同。
  * sources.list: 方便升级。
  * v1.html/v2.html: 版本相关的html文件。
  * myapp-deploy.yaml: deploy文件，修改其中的version和image，会导致pod滚动升级。
  * myapp-svc.yaml: svc文件。
* mysrv: mysrv相关资源。mysrv有状态无版本。
  * mysrv.py: python写的服务。方便读写当前目录。
  * Dockerfile: dockerfile
  * Makefile: `make all`编译到推送镜像。
  * mysrv-sts.yaml: 部署statefulset。
  * mysrv-svc.yaml: svc文件。
* sched: 调度测试有关文件。
  * metrics-server.yaml: 实际上是 https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml 。
  * req-high-pod.yaml: 要求比较高的pod。1C1G。
  * req-low-pod.yaml: 要求比较低的pod。200m CPU + 100m MEM。
  * req-impossible-pod.yaml: 做不到的pod。5C5G。（我穷）
* sec-ctx: 安全隔离有关的文件。具体看`k8s in action`第十三章。
  * file-pod.yaml: 容器内访问主机文件。
  * net-pod.yaml: 容器内访问主机网络（hostNetwork）。
  * pid-pod.yaml: 容器内访问主机PID空间。（ps可见列表）
  * priv-pod.yaml: 容器内拥有特权。

# Kubernetes NFS Subdir External Provisioner

使用一个nfs服务器，创建多个pv来支撑多个pvc的工具。文件参考`nfs-subdir-external-provisioner`目录。

具体看[Kubernetes NFS Subdir External Provisioner](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner)。

# registry

推荐使用registry创建。

```
$ docker pull registry:2
$ docker run -d --name reg --restart=always -p 5000:5000 -v ~/docker/registry:/var/lib/registry registry:2
```

注意几点：

* registry好用难管理。推荐操作是把需要的image推上去。不用了直接把上面那个存储目录全删干净重新推。
* `ip:5000`不大好用，我做了`https://domain/`到`ip:5000`的转发。

几个常见操作。

* list catalogs: `curl https://hub.base.domain/v2/_catalog`
* list tags: `curl https://hub.base.domain/v2/<name>/tags/list`
* list manifest: `curl -s -H 'Accept: application/vnd.docker.distribution.manifest.v2+json' https://hub.base.domain/v2/<name>/manifests/<tag> | jq -r '.config.digest'`
* delete: `curl -s -H "Accept: application/vnd.docker.distribution.manifest.v2+json" -X DELETE https://hub.base.domain/v2/<name>/manifests/<id>`
* gc: `docker exec registry bin/registry garbage-collect --dry-run /etc/docker/registry/config.yml`

# Kubernetes Metrics Server

metric server。部署后top开始工作，可以使用hpa。

具体看[Kubernetes Metrics Server](https://github.com/kubernetes-sigs/metrics-server)。