# deb

安全隔离有关的文件。具体看`k8s in action`第十三章。

# 目录结构和作用解释

* README.md: 本文档
* file-pod.yaml: 容器内访问主机文件。
* net-pod.yaml: 容器内访问主机网络（hostNetwork）。
* pid-pod.yaml: 容器内访问主机PID空间。（ps可见列表）
* priv-pod.yaml: 容器内拥有特权。
