# demo

示例性项目，使用k8s发布一个简单的应用。

# 目录结构和作用解释

* README.md: 本文档
* postgres.yaml: 发布一个示例数据库
  * service
  * secret: password为passwd123
  * sts: 底层使用nfs-client
* redis.yaml: 发布一个示例redis
  * service
  * deploy
* traefik-role.yaml: traefik所需的account和role
  * ClusterRole
  * ServiceAccount
  * ClusterRoleBinding
* traefik-app.yaml: 发布traefik作为ingress
  * Service: traefik-dashboard
  * Service: traefik-web
  * Deployment
* whoami.yaml: traefik的示例性应用，参见[这里](https://doc.traefik.io/traefik/getting-started/quick-start-with-kubernetes/)
  * Service
  * Ingress
  * Deployment

# traefik ing的测试

1. 发布`traefik-role.yaml`。
2. 发布`traefik-app.yaml`。
3. 发布`whoami.yaml`。
4. `kubectl get svc`。
   * 所有节点的IP地址。
   * 其中`traefik-dashboard`对应的端口，直接访问可见traefik dashboard。
   * `whoami`对应端口，可见直接访问whoami的输出。
   * `traefik-web`对应端口，直接访问404。
   * `curl -H 'Host: a.foo.com' -v http://master:traefik-web-port/`，访问可见`whoami`被代理后的页面。
