# 安装

参考[这份手册](https://docs.cilium.io/en/stable/gettingstarted/k8s-install-default/)。

# vxlan

* 为每个pod分配一对lxc*的虚拟网卡，一块在容器内，一块在容器外。
* 出向流量，从对应lxc*虚网卡中出，进入cilium_vxlan设备。
* 入向流量，从cilium_vxlan设备出现，进入lxc*设备。
* 真实网卡可见8472封装流量。
* node上的host路由表完全没有任何用处。
* node到真实网络的masquerade走iptables。

# native

* 为每个pod分配一对lxc*的虚拟网卡，一块在容器内，一块在容器外。这点没区别。
* 出向流量，从lxc*出，进入eth设备。这点和vxlan有本质区别。
* 入向流量，从eth入，进入lxc*设备。
* 出向的投递路由表是真实有效的，入向的过程还是和路由表没有任何关系。
