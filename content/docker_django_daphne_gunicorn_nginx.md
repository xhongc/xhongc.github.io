title: Docker部署应用 Django+daphne+Gunicorn+Nginx+Redis
date: 2020-07-22
author: charles
Tags: docker
Slug: docker-django-daphne-gunicorn-nginx
Category: python

## 前言
这里使用Docker部署应用，用到的技术栈

- Django==2.2.14
- Daphne, 支持HTTP, HTTP2 和 WebSocket 的asgi的服务器，这里主要是处理WebSocket 的请求。
- Gunicorn, green unicorn 简称,unix系统的wsgi http服务器 处理符合wsgi的接口。
- Nginx, 静态资源处理和请求的分发等，http请求指向gunicorn进程，websocket请求指向daphne进程等。
- Docker,  是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的镜像中。

>tips: 这里默认大家已经安装`docker` 和`docker-compose`
## 代码准备
这里使用GitHub上的django-channels实现的websokect项目:
[https://github.com/xhongc/dj-chat](https://github.com/xhongc/dj-chat)

```shell
git clone  https://github.com/xhongc/dj-chat.git
```

## 构建镜像（Dockerfile）

目录结构 

![UqNSv4.png](https://s1.ax1x.com/2020/07/23/UqNSv4.png)

- 项目镜像 `dj-chat/Dockerfile`
```dockerfile
FROM python:3.7

ENV PYTHONUNBUFFERED 1
# 更新apt-get
RUN apt-get update && apt-get install -y gettext python3-dev libpq-dev
RUN mkdir /dj-chat
#设置工作目录
WORKDIR /dj-chat
#将当前目录加入到工作目录中
ADD . /dj-chat

RUN pip install -r /dj-chat/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
RUN python manage.py migrate

EXPOSE 80 8001 8000
```

- #### 构建一个项目的镜像

 `FROM python:3.7` 基于python3.7镜像进行一步一步的叠层操作。
 
 `ENV PYTHONUNBUFFERED 1` 设置系统环境变量
 
 `ADD . /dj-chat`  将当前目录加入到工作目录中
  
 `RUN pip install -r /dj-chat/requirements.txt` 镜像目录已经有了代码 可以开始安装python环境
 
 `RUN python manage.py migrate`迁移数据库
 
 `EXPOSE 80 8001 8000` 暴露端口 之后daphne ，gunicorn服务方便映射
 

- #### Nginx 镜像`dj-chat/nginx/Dockerfile`

```dockerfile
FROM nginx

#对外暴露端口
EXPOSE 80
RUN mkdir -p /home/ubuntu/chat_log
RUN rm /etc/nginx/conf.d/default.conf
ADD ./nginx/nginx-chat.conf  /etc/nginx/conf.d/
ADD ./templates/chat/boot_chat.html  /home/ubuntu/
```

`RUN mkdir -p /home/ubuntu/chat_log` nginx log文件目录，可以自行创建在其他目录。

`RUN rm /etc/nginx/conf.d/default.conf` 移除默认nginx配置。

`ADD ./nginx/nginx-chat.conf  /etc/nginx/conf.d/` 添加自己写的nginx配置

`ADD ./templates/chat/boot_chat.html  /home/ubuntu/` 项目nginx首页index

## 编排镜像（docker-compose）
把各个镜像连结起来
```
version: '3.7'

services:
  redis:
    image: redis
    restart: always
  dj-chat.wsgi:
    build: .
    image: "dj-chat:latest"
    container_name: "dj-chat-g-unicorn"
    command: bash -c "gunicorn -w 1 -k gevent -b 0.0.0.0:8000 dj_chat.wsgi:application"
    ports:
      - "8000:8000"
    depends_on:
      - redis
    links:
      - redis
    expose:
      - "8000"
  dj-chat.asgi:
    image: "dj-chat:latest"
    container_name: "dj-chat-daphne"
    command: bash -c "daphne -b 0.0.0.0 -p 8001 dj_chat.asgi:application"
    ports:
      - "8001:8001"
    depends_on:
      - redis
    links:
      - redis
    expose:
      - "8001"
  nginx:
    build:
      context: .
      dockerfile: ./nginx/Dockerfile
    image: "nginx-chat"
    container_name: "nginx-chat"
    depends_on:
      - dj-chat.asgi
      - dj-chat.wsgi
    volumes:
      - ./static:/home/ubuntu/static
    ports:
    - "80:80"

```

 `version` 对应docker版本todo
 
 `services` 构建各个镜像服务
 
 - `redis` 没有自写Dokcerfile的镜像从官方hub拉取redis服务
 
 - `dj-chat.wsgi`：这里是应用于gunicorn
 
 	- build： 指定Dockerfile 文件位置
 	
 	- image：镜像名称
 	
 	-  container_name：容器名称
 	
 	- command 执行命令启动Gunicorn（注意开的ip是0.0.0.0）
 	
 	- ports： 端口映射（todo）
 	
 	- depends_on： 容器的依赖 ，被依赖的服务会先启动
 	
 	- links ：容器连接 todo
 	
 	- expose 暴露端口
 	
 - `dj-chat.asgi` 应用于daphne
 
 	-  image：使用上面已经构建的镜像，不需要重新
 	
 	-  container_name：容器名称
 	
 	- command 执行命令启动Daphne（注意开的ip是0.0.0.0）
 	
 	- ports： 端口映射（todo）
 	
 	- depends_on： 容器的依赖 ，被依赖的服务会先启动
 	
 	- links ：容器连接 todo
 	
 	- expose 暴露端口

 - `nginx`：构建`dj-chat/nginx/Dockerfile`
 
 	- build：
 	
 		- context 上下文目录
 		
 		- dockerfile：根据上下文目录的dockerfile相对路径
 		
 	-  image：镜像
 	
 	-  container_name：容器名称
 	
 	- depends_on：依赖wsgi和asgi服务
 	
 	- volumes：静态文件挂载在nginx容器里

**expose 和 ports 都可以暴露容器的端口**，
区别是 expose 仅暴露给其他容器，而 ports 会暴露给其他容器和宿主机，像dj-chat.asgi:设置了ports:- "8001:8001" 可以宿主机直接ip：8001 直接访问到。

**坏的**<none>:<none>**镜像**的产生而docker build 或是 pull 命令就会产生临时镜像。如果我们用docker-compose build新镜像后，因为版本更新需要重新创建，那么以前那个版本的镜像就会
成为临时镜像。这个是需要删除的。删除命令见下。

```shell
清除坏的<none>:<none>镜像
docker rmi $(docker images -f "dangling=true" -q)
```

## nginx配置和django配置
- dj-chat/nginx/nginx-chat.conf

`proxy_pass http://dj-chat.wsgi:8000;`
`proxy_pass http://dj-chat.asgi:8001;`
ngixn配置代理host要改成docker-compose的容器名称

- dj-chat/dj-chat/settings
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        'TIMEOUT': 1800,  # 缓存超时时间（默认300，None表示永不过期，0表示立即过期）
        "OPTIONS": {
            "MAX_ENTRIES": 300,  # 最大缓存个数（默认300）
            "CULL_FREQUENCY": 3,  # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
            "CLIENT_CLASS": "django_redis.client.DefaultClient",  # redis客户端
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},  # redis最大连接池配置
            "PASSWORD": "",  # redis密码
        },
        'KEY_PREFIX': '',  # 缓存key的前缀（默认空）
        'VERSION': 2,  # 缓存key的版本（默认1）
    },
}
```
设置LOCATION的HOST要改成docker-compose的容器名称
```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}
```
设置CHANNEL_LAYERS的HOST要改成docker-compose的容器名称redis

## 构建，运行容器
```shell
docker-compose build
docker-compose up -d
```
可以看到容器运行成功，访问127.0.0.1或者你的公网ip可以看到页面。

## 持续开发项目
如果项目还是在快速开发状态，可以把代码挂载卷上
修改
dj-chat/Dockerfile
```dockerfile
FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y gettext python3-dev libpq-dev

RUN mkdir /dj-chat
#设置工作目录
WORKDIR /dj-chat
#将当前目录加入到工作目录中
#ADD . /dj-chat # 挂载卷中可以注释
ADD ./requirements.txt /dj-chat/
RUN pip install -r /dj-chat/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

EXPOSE 80 8001 8000
```

和dj-chat/docker-compose.yml

```yaml
dj-chat.wsgi:
    ...
    volumes:
      - .:/dj-chat
  dj-chat.asgi:
    ...
    volumes:
      - .:/dj-chat
```

由github控制代码更新，`docker-compose restart` 重启容器生效
