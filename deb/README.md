# deb

定义基础镜像。后续一系列实验镜像都是基于`debian:latest`。

# 目录结构和作用解释

* README.md: 本文档
* deb: 里面放了两个基础文件，`proxy`和`sources.list`。允许debian动态升级系统。
* create-deb-cm.sh: 使用deb目录生成对应configmap。
* deb-cm.yaml: 所生成的configmap。
* deb-pod.yaml: 最基本的deb镜像定义的pod。
* deb-apt-pod.yaml: 使用configmap定义的pod，加载了动态升级功能。
