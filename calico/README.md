# calico

* [Calico配置及原理](https://system51.github.io/2020/05/27/using-calico/)

# 目录结构和作用解释

* README.md: 本文档
* calico.yaml: `wget https://docs.projectcalico.org/manifests/calico.yaml`
* default-ipv4-ippool-bgp.yaml: bgp模式的配置，所有node需要在同一个大二层里。（或是网关bgp打通，详见下）
* default-ipv4-ippool-ipip.yaml: ipip模式的配置，可以跨越网关。
* default-ipv4-ippool-vxlan.yaml: vxlan模式的配置。同样进行封装，使用vxlan协议，而非ipip协议。
* calico-*.pcap: 三种模式的抓包结果。

# ipip

* 除去正常路由外的路由表。
```
root@k8s-node1:/home/shell# ip route
blackhole 10.2.36.64/26 proto bird 
10.2.36.68 dev calif5eaaa317d1 scope link 
10.2.36.69 dev cali89dc4914562 scope link 
10.2.36.70 dev califd470b788cc scope link 
10.2.36.71 dev calid2918f95dae scope link 
10.2.169.128/26 via 192.168.33.57 dev tunl0 proto bird onlink 
10.2.235.192/26 via 192.168.33.53 dev tunl0 proto bird onlink 
```
* 本机为`k8s-node1`，IP为`10.2.36.64/26`。68-71指向四个容器，`10.2.169.128/26`指向`192.168.33.57`，即`k8s-node2`。`10.2.235.192/26`指向`192.168.33.53`即`k8s-master`。
* 表面上看，协议为`ipip`，实际上为`ipencap`，序号为4。
* 使用`tcpdump -i enp1s0 -w calico-ipip.pcap proto 4`抓包。
* master上使用`calicoctl node status`，可以看到bgp信息。
* ipip模式(以及calico的所有后续模式)下，node越多，每个node上的路由表项越多。
* ipip模式的寻址关键信息为`[ip range, remote ip]`，该信息写入路由表。

引用：

1. [An introduction to Linux virtual interfaces: Tunnels](https://developers.redhat.com/blog/2019/05/17/an-introduction-to-linux-virtual-interfaces-tunnels)

# bgp

* 修改`IPPool`对象，将`ipipMode`由`Always`，改为`Never`。
* 使用`tcpdump -i enp1s0 -w calico-vxlan.pcap net 10.2.0.0/16`抓包。
* 路由表和ipip模式的区别。
```
10.2.169.128/26 via 192.168.33.57 dev enp1s0 proto bird 
10.2.235.192/26 via 192.168.33.53 dev enp1s0 proto bird 
```
* 在物理网络上，`10.2.x.x`的ip正在直接传输。这一模式能够跑通的前提是，enp1s0网卡上清楚的知道目标设备的Mac地址。
* 如果要经过路由，路由器不知道`10.2.x.x`的传输指向，就会无法工作。
* 通过路由器且能正常工作的前提是，路由器和整个系统BGP Peer。
* 路由器不参与情况下，最大范围是同二层。而一个大二层容易产生广播风暴，因此有尺寸限制。
* ipip模式的寻址关键信息为`[ip range, remote ip]`，该信息写入路由表。与ipip的唯一区别为不带包装头。

# vxlan

* 修改`IPPool`对象，将`ipipMode`由`Always`，改为`Never`。将`vxlanMode`由`Never`改为`Always`。
* 路由表和ipip模式的区别。
```
10.2.169.128/26 via 10.2.169.137 dev vxlan.calico onlink 
10.2.235.192/26 via 10.2.235.193 dev vxlan.calico onlink
```
* 核心输出。
```
# ip a
28: vxlan.calico: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN group default 
    link/ether 66:8c:73:5a:90:99 brd ff:ff:ff:ff:ff:ff
    inet 10.2.36.72/32 scope global vxlan.calico
       valid_lft forever preferred_lft forever
    inet6 fe80::648c:73ff:fe5a:9099/64 scope link 
       valid_lft forever preferred_lft forever
# ip -d link
28: vxlan.calico: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UNKNOWN mode DEFAULT group default 
    link/ether 66:8c:73:5a:90:99 brd ff:ff:ff:ff:ff:ff promiscuity 0 minmtu 68 maxmtu 65535 
    vxlan id 4096 local 192.168.33.55 dev enp1s0 srcport 0 0 dstport 4789 nolearning ttl auto ageing 300 udpcsum noudp6zerocsumtx noudp6zerocsumrx addrgenmode eui64 numtxqueues 1 numrxqueues 1 gso_max_size 65536 gso_max_segs 65535
# bridge fdb show
66:90:43:3d:b3:e7 dev vxlan.calico dst 192.168.33.57 self permanent
66:d5:cf:d3:6b:7e dev vxlan.calico dst 192.168.33.53 self permanent
# arp -a -n | grep vxlan
? (10.2.235.193) at 66:d5:cf:d3:6b:7e [ether] PERM on vxlan.calico
? (10.2.169.137) at 66:90:43:3d:b3:e7 [ether] PERM on vxlan.calico
```
* 过程分析。
  1. `10.2.36.71` -> `10.2.169.136`。
  2. 根据路由表，应交给`vxlan.calico`设备，发往`10.2.169.137`转发。
  3. 远程vxlan设备mac地址为`66:90:43:3d:b3:e7`。(ARP过程/calico写入？)。
  4. 根据fdb表，vxlan的目标ip为`192.168.33.57`。
* 原理分析。
  * 路由表约定为，pod overlay network通信使用vxlan设备。每个node的所有pod有一个网关IP。该IP可在node的annotations里查看`.metadata.annotations.projectcalico.org/IPv4VXLANTunnelAddr`。
  * 所有网关IP可以认为在同一个大二层里。该二层所需的所有信息在arp表和fdb表中。根据这两张表，二层报文可以被包装并发往目标设备。
  * 因此寻址的关键信息为`[ip range, tunnel ip, tunnel mac，remote ip]`，`ip range => tunnel ip`写入路由表，`tunnel ip => tunnel mac`写入arp表，`tunnel mac => remote ip`写入fdb表。

# 结论

* 同大二层，node在100以内，推荐bgp模式。
* 跨网关。推荐同子网使用bgp模式，跨网关使用ipip模式。

# 快速问答

## 容器内如何访问外网？

在每个node上，有个叫做`cali-nat-outgoing`的chain。这个chain会对所有集群内地址到非集群内地址的访问，进行`MASQUERADE`变换（即snat）。在`IPPool`的`natOutgoing`为true的情况下，这一规则打开。这一chain被`cali-POSTROUTING` chain引用，`cali-POSTROUTING` chain被`POSTROUTING` chain引用。

## 如何查看每个node被分配的地址池？

`kc get ipamblocks`，你可以看到地址池集合。地址池的`.spec.affinity`可以看到他的优先节点。下面的属性包括分配信息等等。

## 容器内路由表是什么样子？

```
default via 169.254.1.1 dev eth0
169.254.1.1 dev eth0 scope link
```

实际上这个ip并没有什么意义。用arp工具查看可以发现。

```
169.254.1.1              ether   ee:ee:ee:ee:ee:ee   C                     eth0
node1.lan                ether   ee:ee:ee:ee:ee:ee   C                     eth0
```

实际上，无论是`169.254.1.1`还是`node1.lan`，都是假造的mac地址。反正bgp/ipip模式下也用不着他们。bgp模式下的pod通讯大概是这个样子。

```
pod1                       node1                      node2                      pod2
----------------------------------------------------------------------------------------------
                           52:54:00:85:ff:19          52:54:00:b2:72:8d
10.2.36.68                 192.168.33.55              192.168.33.57              10.2.169.130
----------------------------------------------------------------------------------------------
 --src:xx:xx:xx:xx:xx:xx->
 --dst:ee:ee:ee:ee:ee:ee->
 --src:10.2.36.68       ->
 --dst:10.2.169.130     ->
                            --src:52:54:00:85:ff:19->
                            --dst:52:54:00:b2:72:8d->
                            --src:10.2.36.68       ->
                            --dst:10.2.169.130     ->
                                                       --src:ee:ee:ee:ee:ee:ee->
                                                       --dst:xx:xx:xx:xx:xx:xx->
                                                       --src:10.2.36.68       ->
                                                       --dst:10.2.169.130     ->
----------------------------------------------------------------------------------------------
                                                       <-src:xx:xx:xx:xx:xx:xx--
                                                       <-dst:ee:ee:ee:ee:ee:ee--
                                                       <-src:10.2.169.130     --
                                                       <-dst:10.2.36.68       --
                            <-src:52:54:00:b2:72:8d--
                            <-dst:52:54:00:85:ff:19--
                            <-src:10.2.169.130     --
                            <-dst:10.2.36.68       --
 <-src:ee:ee:ee:ee:ee:ee--
 <-dst:xx:xx:xx:xx:xx:xx--
 <-src:10.2.169.130     --
 <-dst:10.2.36.68       --
----------------------------------------------------------------------------------------------
```

## networkpolicies找不到？

这个是因为`networkpolicies`和系统资源重名。

可以用`kubectl get crds -A`列出所有crd。然后用`kc get networkpolicies.crd.projectcalico.org -A`来访问。

引用：

1. [Kubernetes: cannot see network policies created with calico](https://stackoverflow.com/questions/72789084/kubernetes-cannot-see-network-policies-created-with-calico)
