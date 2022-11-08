# deb

定义基础镜像。后续一系列实验镜像都是基于`debian:latest`。

# 目录结构和作用解释

* README.md: 本文档
* apt: 里面放了两个基础文件，`proxy`和`sources.list`。允许动态升级系统。
* apt-cm-create.sh: 使用apt目录生成对应configmap。
* apt-cm.yaml: 所生成的configmap。
* base-pod.yaml: 最基本的deb镜像定义的pod。
* cm-pod.yaml: 使用configmap定义的pod，加载了动态升级功能。
