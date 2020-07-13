title: 使用 Python 在 GitHub 上运行你的博客
date: 2020-07-12
author: charles
Tags: pelican
Slug: pelican_course

每个入门程序员或多都想拥有一个自己博客站点，苦于高额的服务器费用和较为麻烦的操作步骤，你完全可以通过 GitHub Pages来实现一个免费，可定制的书写，记录生活，技术分享的平台。
## 为什么使用 GitHub Pages
- 首先它是完全免费，可以省下一笔服务费
- 无须自己购买云服务进行搭建，只需按步骤一步步操作即可，即使你不懂他的技术细节；
- 支持的功能多，玩法丰富，你可以绑定你的域名、使用免费的 HTTPS、自己 DIY 网站的主题、使用他人开发好的插件等等
- 当完成搭建后，你只需要专注于文章创作就可以了，其他诸如环境搭建、系统维护、文件存储的事情一概不用操心，都由 GitHub 处理
## Github中创建一个仓库
选择创建一个新的 Repository  在 Repository name 的位置填写域名，格式是 username.GitHub.io
## 安装 Pelican
`pip install pelican ghp-import Markdown`
将这个刚创建空 Git 仓库克隆到本地：
`git clone <https://GitHub.com/username/username.github.io> blog`
`cd blog`
## 使用Pelican 生成静态页面
在 GitHub 上发布 Web 内容有一个不太引入注意的技巧，对于托管在名为 username.github.io 的仓库的用户页面，其内容由 master 分支提供服务。

我强烈建议所有的 Pelican 配置文件和原始的 Markdown 文件都不要保留在 master 中，master 中只保留 Web 内容。因此，我将 Pelican 配置和原始内容保留在一个我喜欢称为 content 的单独分支中。（你可以随意创建一个分支，但以下内容沿用 content。）我喜欢这种结构，因为我可以放弃掉 master 中的所有文件，然后用 content 分支重新填充它。
`git checkout -b content`

### 配置Pelican
安装完Pelican 提供初始化工具 pelican-quickstart 来创建博客的初始配置
```
$ pelican-quickstart
Welcome to pelican-quickstart v3.7.1.

This script will help you create a new Pelican-based website.

Please answer the following questions so this script can generate the files
needed by Pelican.

> Where do you want to create your new web site? [.]  
> What will be the title of this web site? Super blog
> Who will be the author of this web site? username
> What will be the default language of this web site? [en]
> Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) n
> Do you want to enable article pagination? (Y/n)
> How many articles per page do you want? [10]
> What is your time zone? [Europe/Paris] UTC
> Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n) y
> Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n) y
> Do you want to upload your website using FTP? (y/N) n
> Do you want to upload your website using SSH? (y/N) n
> Do you want to upload your website using Dropbox? (y/N) n
> Do you want to upload your website using S3? (y/N) n
> Do you want to upload your website using Rackspace Cloud Files? (y/N) n
> Do you want to upload your website using GitHub Pages? (y/N) y
> Is this your personal page (username.github.io)? (y/N) y
Done. Your new project is available at /Users/username/blog
```
Pelican 会为你创建以下目录
```
Makefile      content/     develop_server.sh*
fabfile.py    output/      pelicanconf.py
publishconf.py
```
### 提交content 分支
将所有 Pelican 生成的文件添加到本地 Git 仓库的 content 分支，提交更改，然后将本地更改推送到 Github 上托管的远程仓库：
```
$ git add .
$ git commit -m 'initial pelican commit to content'
$ git push origin content
```
### 提交一篇文章测试一下
`cd content` content 目录存放markdown格式的文章
让我新建first-post.md
```
title: 使用 Python 在 GitHub 上运行你的博客
date: 2020-07-12
author: charles
Tags: pelican
Slug: pelican_course

使用 Pelican 创建博客，这是一个基于 Python 的平台，与 GitHub 配合的不错。
```
date：发布时间 ,`pelicanconf.py`文件可以设置 `DEFAULT_DATE_FORMAT = '%Y-%m-%d'` 时间格式化
author : 作者
Tags：标签
Slug： 用于文章生成url的。不添加这个字段话，默认是拼音的url。但是有时侯拼音是错误的，而且对于搜索引擎很不友好
### 发布
- 运行 Pelican 以在 output 中生成静态 HTML 文件：
`$ pelican content -o output -s publishconf.py`
- 使用 ghp-import 将 output 目录的内容添加到 master 分支中：
`$ ghp-import -m "Generate Pelican site" --no-jekyll -b master output`
- 将本地 master 分支推送到远程仓库：
`$ git push origin master`
- 提交新内容并将其推送到 content 分支
`$ git add content $ git commit -m 'added a first post, a photo and an about page' $ git push origin content`
### 完成
打开浏览器输入https://username.github.io 就可以看到博客内容。

### 定制blog
进一步定制博客配置
1. 独立域名 
购买域名映射到https://username.github.io之后在output目录下，创建CNAME文件。内容就是你购买的域名。因为github pages只允许CNAME中的域名映射。
2. 定制主题
找到自己喜欢的pelican主题，[主题地址点我](https://github.com/getpelican/pelican-themes)
3. 关于我
这个就像相当于一个自我介绍的页面，所以就需要在content目录下创建一个pages目录，然后把你要展示的内容放到pages目录下就可以了。
