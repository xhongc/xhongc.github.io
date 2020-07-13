#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'charles'
SITENAME = '少年白'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'UTC'

DEFAULT_LANG = 'Chinese (Simplified)'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          )

# Social widget
SOCIAL = (('Django-chat', 'http://106.55.162.109/'),
          ('Github', 'https://github.com/xhongc'),)

DEFAULT_PAGINATION = 10
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
THEME = 'pelican-bootstrap3'
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
# PLUGIN_PATHS = ['/Users/xiehongchao/Downloads/pelican-plugins-master']
PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['i18n_subsites', 'tag_cloud']
# BOOTSTRAP_THEME = 'yeti'
PYGMENTS_STYLE = 'friendly'
BANNER_ALL_PAGES = False
# BANNER_SUBTITLE = 'Yes wo code!'
BANNER = 'images/b1.jpg'
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
RECENT_POST_COUNT = 5
# SIDEBAR_IMAGES = ['https://s1.ax1x.com/2020/07/11/Ullf56.th.png', ]
FAVICON = 'images/flower.png'
AVATAR = 'images/flower.png'
# TAGS_URL = 'python.html'
DISPLAY_TAGS_ON_SIDEBAR = True
# https://pelican-docs-chs.readthedocs.io/en/latest/
# https://github.com/DandyDev/pelican-bootstrap3/wiki/Variables
DISPLAY_SERIES_ON_SIDEBAR = True
SERIES_TEXT = 'Part %(index)s of the %(name)s series'
TAG_CLOUD_STEPS = 8  # font size
TAG_CLOUD_MAX_ITEMS = 100
TAG_CLOUD_SORTING = 'random'
TAG_CLOUD_BADGE = True
