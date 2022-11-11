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
