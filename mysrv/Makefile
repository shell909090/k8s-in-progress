### Makefile --- 

## Author: shell909090@gmail.com
## Version: $Id: Makefile,v 0.0 2022/02/17 03:57:33 shell Exp $
## Keywords: 
## X-URL: 

REMOTE_REPO=hub.base.domain/mysrv
TAG=latest

all: clean build push

build:
	docker build -f Dockerfile -t $(REMOTE_REPO):$(TAG) --squash .

run:
	docker run -it --rm -p 8000:80 $(REMOTE_REPO):$(TAG)

push:
	docker push $(REMOTE_REPO):$(TAG)

clean:
	- docker rmi $(REMOTE_REPO):$(TAG)

### Makefile ends here
