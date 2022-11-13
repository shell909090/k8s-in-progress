# deb

定义基础镜像。

# 目录结构和作用解释

* README.md: 本文档
* alpine-pod.yaml: 最基本的alpine镜像定义的pod。
* deb: 里面放了两个基础文件，`proxy`和`sources.list`。允许debian动态升级系统。
* create-deb-cm.sh: 使用deb目录生成对应configmap。
* deb-cm.yaml: 所生成的configmap。
* deb-pod.yaml: 最基本的debian镜像定义的pod。
* deb-apt-pod.yaml: 使用configmap定义的pod，加载了动态升级功能。
* ubt-pod.yaml: 最基本的ubuntu镜像定义的pod。

# 四个镜像的区别

* busybox: 1.24M，1B下载，2.8kstar。没有libc，命令行工具都是busybox的分身。
  * busybox-glibc: 4.86M。标准glibc。命令行工具都是busybox的分身。
* alpine: 5.54M，1B下载，9.4kstar。带有musl，libssl，有完整的命令行工具（虽然很多都是busybox）。
* ubuntu: 77.8M，1B下载，10kstar。标准glibc，有完整的系统和工具链，例如有bash。
* debian: 124M，500M下载，4.5kstar。标准glibc，有完整的系统和工具链。
  * debian-slim: 69.3M。标准glibc，有完整的系统和工具链。也有bash。

选择：

1. 最简系统系列。
   1. 如果对系统完全无要求。可以选择busybox。代价就是啥都没有。
   2. 如果需要加装包，可以接受没有glibc。可以选择alpine。代价就是用musl。
   3. 如果不需要加装包，需要glibc。可以选择busybox:glibc。代价就是没什么工具，且不能额外装包。
   4. 如果要额外装包，又要glibc。可以选择使用alpine，加装gcompat。代价就是要自己定制一个镜像。
2. 如果要一个相对完整的系统和工具链，不在乎系统是不是“最小化”。可以选择ubuntu/debian。
   1. debian和ubuntu不对标。ubuntu有额外做最小化的动作，debian-slim才和ubuntu对标。
   2. 即便如此，也不推荐使用debian。因为在中国默认的镜像不方便访问，需要额外调整并自己打一个镜像。直接使用ubuntu一次性搞定两个问题。
3. 其实大部分image，要么用debian，要么带一个alpine的tag。前者是因为debian的dfsg有助于避免纠纷，后者是因为小。以postgres为例，14标准376M，14-alpine216M。
