# 快速问答

Q: 镜像如何查看？
A: 主机上`ctr -n k8s.io i ls`。

Q: 容器如何查看？
A: 主机上`ctr -n k8s.io c ls`。

Q: 容器和pod对应关系？
A:
- 在主机上`ctr -n k8s.io c info <ctrid>`，在Labels可以看到容器所属的pod信息。
- `kubectl -o yaml <pod>`，在`.status.containerStatuses[].containerID`，可以看到ctrid。
- 主机上会有多个`k8s.gcr.io/pause:3.6`所运行容器，这是基础容器，负责保持ns。
