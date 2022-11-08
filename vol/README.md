# vol

卷挂载有关的实验。

# 目录结构和作用解释

* README.md: 本文档
* nfs-pvc.yaml: 基础pvc，创建了`nfs`，申请了10G存储。
* nfs-pv.yaml: 基础pv，使用nfs作为底层存储。
* nfs-subdir-pvc.yaml: pvc，创建里`nfs-subdir`, 使用`nfs-client`作为storage class，申请1G存储。
* vol-git-pod.yaml: 使用`gitRepo`作为底层存储挂载。需要node上安装git。
* vol-hostpath-pod.yaml: 使用`hostPath`作为底层存储。
* vol-nfs-pod.yaml: 使用`nfs`作为底层存储。
* vol-pvc-nfs-pod.yaml: 使用pvc `nfs`作为底层存储。
* vol-pvc-nfs-subdir-pod.yaml: 使用pvc `nfs-subdir`作为底层存储。
