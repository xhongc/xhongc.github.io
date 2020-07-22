title: Docker 镜像修改和提交
date: 2020-07-22
author: charles
Tags: docker
Slug: docker-image-modify
Category: python

> 当你发现构建的镜像缺少python模块，可以进入镜像修改


<hr>
1.启动镜像

- docker run -it "<镜像ID>" /bin/bash
- 修改...
- `exit`
<hr>

2.提交修改

- 容器ID = 修改后docker ps -l 查看生成的容器ID
- docker commit "<容器ID>" image_name:tag
<hr>
查看镜像已经有了修改

