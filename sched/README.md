# 目录结构和作用解释

* README.md: 本文档
* metrics-server.yaml: 实际上是 https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml 。
* req-high-pod.yaml: 要求比较高的pod。1C1G。
* req-low-pod.yaml: 要求比较低的pod。200m CPU + 100m MEM。
* req-impossible-pod.yaml: 做不到的pod。5C5G。（我穷）

# cgroup目录结构

* cgroup位置: `/sys/fs/cgroup/kubepods.slice`。
* `kubepods-besteffort.slice`和`kubepods-burstable.slice`有独立目录，guaranteed没看到。
* 主要是因为该节点(k8s-node1)上跑的只有两类qos等级。
* 当qos等级有guaranteed存在时，没有guaranteed目录。相反，在`/sys/fs/cgroup/kubepods.slice`下面直接建立出了pod目录，层级少了一级。
* `kubepods-burstable.slice`下会有pod对应id的目录，其下有container对应id的目录。最后一个目录中有实际生效的pid。pod目录下和更上级中的pid列表皆为空。
* pod的id在`kubectl get -o yaml pod/[name] -n [namespace]`里面，看`.metadata.uid`。
* pod下面的container目录，并不是这个pod的所有容器。`for line in $(ctr -n k8s.io c ls -q); do echo $line; ctr -n k8s.io c info $line | jq '.Labels'; done`可以看到所有id和所属pod。
* 实际的path，可以用`ctr --namespace k8s.io c info <ctrid>`查询容器信息，`.Spec.linux.cgroupsPath`确定了真实path。
* 确实有部分container，Labels里说属于某个pod，cgroup path也有，但是`/sys/fs/cgroup/`下面找不到内容。

# cgroup官方文档

* cpu.weight的官方文档：[cgroup-v2](https://www.kernel.org/doc/Documentation/cgroup-v2.txt)。
* cgroup.procs: 生效进程。
* cpu.max: 配额。在后者的时间里，最多能占用前者的量。一般后者为100000。设定cpu为500m的话，前者为50000。
* cpu.weight: 调度权重。
* memory.max: 配额，单位为字节。

# pod设定

* requests设定主要影响调度，基本不影响cgroup。只会调整`cpu.weight`和`cpu.weight.nice`。因此requests的设定不影响memory争抢能力，oom依然会按照oom_score来计算kill。
* // WHY: 为啥文档说oom会先杀besteffort？
* limits的cpu影响`cpu.max`，memory影响`memory.max`。

# 实验

* node双核。
* 在一个node上开三个pod，每个都用`dd if=/dev/zero of=/dev/null`跑满cpu。
* 第一个pod为1000m，第二三个pod为200m。
* 三者CPU分配比例为100:50:50。
* CPU的理论分配比例为1000:200:200。
* dd只能吃满一个核心，因此第一个pod占用为100。
* 剩余的CPU被剩下两者均分，为50:50。
