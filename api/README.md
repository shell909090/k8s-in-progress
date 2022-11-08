# api

都是k8s api访问的例子。

# 目录结构和作用解释

* README.md: 本文档
* ambassador.yaml: 两个containers，一个来自`luksa/kubectl-proxy`，一个是标准的debian。标准debian中，可使用curl访问本机8001端口，来访问k8s api而免去认证。具体参考`k8s in action`的`8.2.3`节。
* curl-env.sh: 如何使用标准的curl来直接访问k8s api。
* downward-pod.yaml: downward api的例子。
