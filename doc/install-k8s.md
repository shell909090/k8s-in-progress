# 建立k8s-base实例

建立虚拟机，安装标准debian镜像。保证spec至少1C1G。随后执行以下步骤，建立k8s模板镜像。

1. 关闭防火墙。
2. 安装容器运行时 [1] [2]。
   1. 配置模块`overlay`和`br_netfilter`。
   2. 配置sysctl。
   3. 确认cgroup版本: `grep cgroup /proc/filesystems`。对于`cgroup2`以上，推荐使用systemd cgroup驱动。
   4. 安装containerd [3] [4]:
      1. `aptitude install -y ca-certificates curl gnupg lsb-release`
	  2. `mkdir -p /etc/apt/keyrings`
	  3. `curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg`
	  4. `echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
	  5. `aptitude install -y containerd.io`
   5. 注释`/etc/containerd/config.toml`中的`disabled_plugins = ["cri"]`。
   6. 安装包: `aptitude install -y jq git nfs-common net-tools iproute2`。可选。这是为了支持后面的多项实验。
   7. 安装kubectl, kubelet, kubeadm [5]。
      1. `aptitude install -y apt-transport-https ca-certificates curl`
	  2. `curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg`
      3. `echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | tee /etc/apt/sources.list.d/kubernetes.list`
	  4. `aptitude install -y kubelet kubeadm kubectl`
   8. 打开`SystemdCgroup` [6]。具体配置见下。
      1. 重启containerd: `systemctl restart containerd`
	  2. 检查配置`crictl info | jq '.config.containerd.runtimes.runc'`

SystemdCgroup配置，位置`/etc/containerd/config.toml`，来源 [6]:

```
version = 2

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
  # setting runc.options unsets parent settings
  runtime_type = "io.containerd.runc.v2"
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
    SystemdCgroup = true
```

引用：

1. [Container Runtimes](https://kubernetes.io/docs/setup/production-environment/container-runtimes/)
2. [容器运行时](https://kubernetes.io/zh-cn/docs/setup/production-environment/container-runtimes/)
3. [Getting started with containerd](https://github.com/containerd/containerd/blob/main/docs/getting-started.md)
4. [Install Docker Engine on Debian](https://docs.docker.com/engine/install/debian/)
5. [Installing kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
6. [Switching to Unified Cgroups](https://flatcar-linux.org/docs/latest/container-runtimes/switching-to-unified-cgroups/)

# 建立集群

1. 将k8s-base复制为k8s-master, k8s-node1, k8s-node2。
   * 保证双核2G
   * 修改`/etc/hostname`和`/etc/hosts`，调整主机名。注意不要用`hostnamectl set-hostname`，或者不要只用。`/etc/hosts`不会调整。
2. `kubeadm init` [1]。
   * 配置文件`/etc/kubernetes/admin.conf`。kubectl会使用这个文件来链接控制平面。
   * `kubeadm join 192.168.33.53:6443 --token a --discovery-token-ca-cert-hash sha256:b`
3. 安装calico [2]。
   1. `wget https://docs.projectcalico.org/manifests/calico.yaml`
   2. `kubectl apply -f calico.yaml`

引用：

1. [Creating a cluster with kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
2. [Easy steps to install Calico CNI on Kubernetes Cluster](https://www.golinuxcloud.com/calico-kubernetes/)
