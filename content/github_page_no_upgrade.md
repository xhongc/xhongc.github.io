title: Github Pages不能自动更新
date: 2020-07-13
author: charles
Tags: github
Slug: github_page_no_upgrade
Category: python

刚刚往github pages的repository里提交了一篇文章后，却发现github pages的页面一直没有更新——看不到新提交的文章。网上搜了一些资料，最后解决了这个问题。

一般来说，只要你的github pages repository有新的提交，github的服务器就会运行jekyll编译你的repository（延时很小）。如果编译出错，那么你的github pages页面是不会更新的；同时，github也会给你发一封提醒邮件，大致内容如下，

```
The page build failed for the `master` branch with the following error:

Unable to build page. Please try again later.

For information on troubleshooting Jekyll see:

  https://help.github.com/articles/troubleshooting-jekyll-builds

```

给出的错误信息很有限，仅仅通知你编译出错。

### 要找到出错的原因
- 首先确认下github pages服务有没有down掉或被降级；查看这个网址，[https://www.githubstatus.com/](https://www.githubstatus.com/)，可以了解服务器的运行状态。
- 如果服务器运行良好，那么极有可能是提交的内容有错误。 可以在本地用jekyll编译一下repository，看看是否有错误。

首先，更新一下本地的jekyll。github可能使用了较新版本的jekyll，所以即使你使用以前的本地jekyll编译没有问题，远端的jekyll编译时也可能出错。（当然，最好是保证本地和远端的jekyll版本一样。但是，还没有发现查看远端jekyll版本的方法。）

$ sudo gem install jekyll
$ jekyll --version 然后，在本地编译你的repository。

$ jekyll build --safe jekyll --trace 给出的出错信息还是很详细的，能看出在什么位置发生了错误。
查看错误信息并修改

我是正好遇到Github Pages 降级，等github修复后可以正常了
