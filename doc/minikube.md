# 快速问答

## 怎么查看pod的image大小？

`kubectl get -o yaml node/minikube`

## 为什么minikube的pod不在docker的ps里？

minikube连接了另一个docker: `eval $(minikube docker-env)`。这个环境指向了一个独立的network: `docker network inspect minikube`。使用这个network的容器的image为`gcr.io/k8s-minikube/kicbase:v0.0.29`。

实际是在docker container里，跑了一个containerd。随后启动的所有镜像都在这个新的containerd里。该容器持久化了所有的`/var`下内容。容器内的containerd和容器外的版本可以不一致。为了启动containerd，容器以`Privileged: true`执行。该容器mount了一个hostpath: `/var/lib/docker/volumes/minikube/_data`。

## docker的image存放在哪里？

docker的image存放在`/var/lib/docker/overlay2`下面。

## minikube的pod存放在哪里？

minikube的pod就存放在 `/var/lib/docker/volumes/minikube/_data/lib/docker/overlay2`下面。

## containerd.io是什么？

containerd vs docker: [一文搞懂容器运行时 Containerd](https://www.qikqiak.com/post/containerd-usage/)。
