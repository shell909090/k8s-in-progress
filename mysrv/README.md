# mysrv

mysrv是一个有状态服务。用于显示当前目录的文件列表，上传，删除。

# 用法

```
$ python3 mysrv.py
```

* 访问当前地址的80端口，可见所有文件。
* `curl http://localhost/`，可见文件列表。
* `curl http://localhost/mysrv.py`，可以下载文件内容。
* `curl -X POST --data-binary @[filename] http://localhost/[filename]`，可上传文件。
* `curl -X DELETE http://localhost/[filename]`，可删除文件。

# 目录结构和作用解释

* README.md: 本文档
* mysrv.py: python写的服务。方便读写当前目录。
* Dockerfile: dockerfile
* Makefile: `make all`编译到推送镜像。
* mysrv-sts.yaml: 部署statefulset。
* mysrv-svc.yaml: svc文件。
