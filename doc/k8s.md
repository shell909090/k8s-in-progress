# 快速问答

## 镜像如何查看？

主机上`ctr -n k8s.io i ls`。

## 容器如何查看？

主机上`ctr -n k8s.io c ls`。

## 容器和pod对应关系？

- 在主机上`ctr -n k8s.io c info <ctrid>`，在Labels可以看到容器所属的pod信息。
- `kubectl -o yaml <pod>`，在`.status.containerStatuses[].containerID`，可以看到ctrid。
- 主机上会有多个`k8s.gcr.io/pause:3.6`所运行容器，这是基础容器，负责保持ns。

## svc如何转发到服务？

三种模式[Service](https://kubernetes.io/docs/concepts/services-networking/service/)。

1. User space proxy mode（未测试）。
2. IPVS proxy mode（未测试）。
3. iptables proxy mode （关注nat表的KUBE-SERVICES链，NodePort关注KUBE-NODEPORTS链）:

```
Chain KUBE-SVC-TCOU7JCQXEZGVUNU (1 references)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 KUBE-SEP-SKLOGSUPQB2HSQ77  all  --  *      *       0.0.0.0/0            0.0.0.0/0            /* kube-system/kube-dns:dns -> 10.2.36.68:53 */ statistic mode random probability 0.50000000000
    0     0 KUBE-SEP-BIJ27KOW3FV2C4IP  all  --  *      *       0.0.0.0/0            0.0.0.0/0            /* kube-system/kube-dns:dns -> 10.2.36.70:53 */
```

## NodePort和普通Service的区别？

没有区别。普通Service将目标为`<某个虚拟IP>:<目标端口>`的报文，转发到`<实际podIP>:<实际目标端口>`。NodePort将`<local>:<临时分配端口>`，转发到`<实际podIP>:<实际目标端口>`。

## 自己搭建的集群上使用LB模式的svc会发生什么？

pending

# k8s如何使用gitRepo/nfs？

node上需要自己装一个git/nfs-common。

## 域名解析如何工作？

每个pod上都有一个`/etc/resolv.conf`文件，其中指明一个集群IP。包含了三个默认搜索域。

* [namespace].svc.cluster.local
* svc.cluster.local
* cluster.local

集群IP指向kube-dns或者core-dns。两者从apiserver获得所有信息，更新。

## 如何使用etcdctl连接k8s的etcd看数据？

参考这里: [使用 etcdctl 访问 Kubernetes 数据](https://jimmysong.io/kubernetes-handbook/guide/using-etcdctl-to-access-kubernetes-data.html)

```
ETCDCTL_API=3 etcdctl --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/peer.crt \
  --key=/etc/kubernetes/pki/etcd/peer.key \
  get /registry/namespaces/default -w=json | jq .
```

## etcd的容量查询？

```
ETCDCTL_API=3 bin/etcdctl --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/peer.crt --key=/etc/kubernetes/pki/etcd/peer.key endpoint status --write-out=table
```

## controller是啥？

监听某个对象的改变，然后跟着调整其他对象。例如deploy的controller，监听deploy的改变事件，并且创建rs对象，滚动。

# CNI对比

* https://kubevious.io/blog/post/comparing-kubernetes-container-network-interface-cni-providers
* https://kubernetes.io/docs/concepts/cluster-administration/networking/

# Kubernetes Metrics Server

metric server。部署后top开始工作，可以使用hpa。

具体看[Kubernetes Metrics Server](https://github.com/kubernetes-sigs/metrics-server)。
