# node失效和迁移测试

# 强制关闭节点并迁移到新节点测试

1. node2启动，探知时间，30s以内。
2. node1关机，探知时间，1分钟。
3. 5分钟后。
    - rs启动新pod。老pod terminating。
    - sts terminating。
4. deploy正常迁移，sts一直没起来。
5. drain node没有效果。
6. delete pod，一直block，超过30s也不成功。
7. delete --force pod成功。
8. sts原pod被delete后立刻在node2重建。deploy的pod就直接没了。
9. 原node重启后，`kubectl describe`会出现有不应当存在的pod的情况。很快恢复。

# 关闭节点再启动原节点测试

1. node1启动，探知时间，30s以内。
2. node2关机，探知时间，1分钟。
3. 5分钟后。
    - rs启动新pod。老pod terminating。
    - sts terminating。
4. deploy正常迁移，sts一直没起来。
5. 启动node2。
6. 状态保持一段时间后。
    - sts的pod进入pending，随后ContainerCreating，重新启动。维持在原node上。
    - deploy的pod直接结束。

# coredns的特殊性

* coredns的owner是rs。
* etcd，kube-apiserver，kube-controller-manager，kube-scheduler的owner是node。
* coredns有tolerations。`node-role.kubernetes.io/master`
* coredns干掉一个pod后会迁移到node2。

结论：coredns是一个普通应用，但可以跑在master上，以防所有node下线。

# 原因分析

1. step3里面等待五分钟的原因：
```
Tolerations:
- node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
- node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
```
2. sts没起来的原因。sts和deploy行为不同。deploy需要维持“有效副本数”。sts维持总副本数。[这里](https://kubernetes.io/docs/tutorials/stateful-application/basic-stateful-set/)描述了一个更特殊的例子。
3. “强制关闭节点并迁移到新节点测试”测试的step9，可能说明kubelet本地是存了数据的。

# drain node优雅关闭

1. `kubectl drain --ignore-daemonsets node2`。
2. node2关机。
3. `kubectl uncordon node2`，把不可调度去了。
4. pod迁移几乎无感知。客户端可以正常使用。
5. `kubectl describe pod`能看到有重启记录。
