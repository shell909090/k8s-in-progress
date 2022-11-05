# myapp

myapp有两个版本，v1和v2。两个版本皆为nginx镜像加上一个文件。在访问http的时候可以鉴别出当前是哪个版本。

myapp用来测试deploy rolling过程。

# 目录结构和作用解释

* README.md: 本文档
* Dockerfile-v1/Dockerfile-v2: dockerfile
* Makefile: 编译文件。`make build_v1`编译第一个版本，`make build_v2`编译第二个。`push_v1`和`push_v2`同。
* sources.list: 方便升级。
* v1.html/v2.html: 版本相关的html文件。
* myapp-deploy.yaml: deploy文件，修改其中的version和image，会导致pod滚动升级。
* myapp-svc.yaml: svc文件。
