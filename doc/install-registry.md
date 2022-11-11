# 安装registry

# 为什么需要私有registry

快

# choose a private registry

* docker的registry [1]。
  * 对象很难删除。
* nexus3 [2] [3] [4]。
  * 4C2G，资源需求很高。
  * 需要一个独立端口，或者一个独立域名。
* aws/alicloud容器镜像服务。
  * 要钱。
  * 穷是我的缺点，不是他们的。

引用：

1. [Deploy a registry server](https://docs.docker.com/registry/deploying/)
2. [install](https://hub.docker.com/r/sonatype/nexus3)
3. [使用](https://yeasy.gitbook.io/docker_practice/repository/nexus3_registry)
4. [How to upload and download docker images using nexus registry/repository?](https://www.devopsschool.com/blog/how-to-upload-and-download-docker-images-using-nexus-registry-repository/)

# registry

推荐使用registry创建。

```
$ docker pull registry:2
$ docker run -d --name reg --restart=always -p 5000:5000 -v ~/docker/registry:/var/lib/registry registry:2
```

注意几点：

* registry好用难管理。推荐操作是把需要的image推上去。不用了直接把上面那个存储目录全删干净重新推。
* `ip:5000`不大好用，我做了`https://domain/`到`ip:5000`的转发。

几个常见操作。

* list catalogs: `curl https://hub.base.domain/v2/_catalog`
* list tags: `curl https://hub.base.domain/v2/<name>/tags/list`
* list manifest: `curl -s -H 'Accept: application/vnd.docker.distribution.manifest.v2+json' https://hub.base.domain/v2/<name>/manifests/<tag> | jq -r '.config.digest'`
* delete: `curl -s -H "Accept: application/vnd.docker.distribution.manifest.v2+json" -X DELETE https://hub.base.domain/v2/<name>/manifests/<id>`
* gc: `docker exec registry bin/registry garbage-collect --dry-run /etc/docker/registry/config.yml`
