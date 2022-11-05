### Makefile --- 

## Author: shell909090@gmail.com
## Version: $Id: Makefile,v 0.0 2022/02/17 03:57:33 shell Exp $
## Keywords: 
## X-URL: 

REMOTE_REPO=hub.base.domain/myapp

all: clean_images build_v1 build_v2 push_v1 push_v2

build_v1:
	docker build -f Dockerfile-v1 -t $(REMOTE_REPO):v1 --squash .

build_v2:
	docker build -f Dockerfile-v2 -t $(REMOTE_REPO):v2 --squash .

push_v1:
	docker push $(REMOTE_REPO):v1

push_v2:
	docker push $(REMOTE_REPO):v2

clean_images:
	- docker rmi $(REMOTE_REPO):v1
	- docker rmi $(REMOTE_REPO):v2

### Makefile ends here
