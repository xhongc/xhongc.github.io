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
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         )

# Social widget
SOCIAL = (('Django-chat', 'http://106.55.162.109/'),
          ('Github', 'https://github.com/xhongc'),)

DEFAULT_PAGINATION = 10
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
THEME = '/Users/xiehongchao/Downloads/pelican-themes-master/pelican-bootstrap3'
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
PLUGIN_PATHS = ['/Users/xiehongchao/Downloads/pelican-plugins-master']
PLUGINS = ['i18n_subsites']
