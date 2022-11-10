# deb

定义基础镜像。后续一系列实验镜像都是基于`debian:latest`。

同时定义了基于`ubuntu:latest`的镜像。基于ubuntu的镜像不需要修改mirrors和proxy就可以很好的工作，而且体积也更小。xs

# 目录结构和作用解释

* README.md: 本文档
* deb: 里面放了两个基础文件，`proxy`和`sources.list`。允许debian动态升级系统。
* create-deb-cm.sh: 使用deb目录生成对应configmap。
* deb-cm.yaml: 所生成的configmap。
* deb-pod.yaml: 最基本的debian镜像定义的pod。
* deb-apt-pod.yaml: 使用configmap定义的pod，加载了动态升级功能。
* ubt-pod.yaml: 最基本的ubuntu镜像定义的pod。
