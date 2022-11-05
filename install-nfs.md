# 搭建nfs

基于一台debian虚拟机，安装nfs服务器

1. open port 111,2049 in both TCP and UDP
2. `apt install nfs-kernel-server`
3. `/etc/exports`
   * `/srv/nfs	192.168.0.0/24(rw,no_root_squash,no_subtree_check)`
4. `/etc/hosts.allow`
   * `portmap: 192.168.0.`
5. `exportfs -a`
6. `systemctl restart nfs-server`
7. test from client
   1. `aptitude install -y nfs-common`
   2. `sudo mount 192.168.33.45:/srv/nfs nfs/`

引用：

1. [NFS Server Setup](https://wiki.debian.org/NFSServerSetup)

# Kubernetes NFS Subdir External Provisioner

使用一个nfs服务器，创建多个pv来支撑多个pvc的工具。文件参考`nfs-subdir-external-provisioner`目录。

具体看[Kubernetes NFS Subdir External Provisioner](https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner)。
