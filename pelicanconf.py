#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Alexander Kamyanskiy'
SITENAME = 'kamyanskiy.github.io'
SITEURL = 'https://kamyanskiy.github.io'

PATH = 'content'

TIMEZONE = 'Europe/Moscow'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

GITHUB_USER = 'kamyanskiy'

THEME="pelican-themes/pelican-bootstrap3/"
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
PLUGIN_PATHS = ['pelican-plugins/'] 
PLUGINS = ['i18n_subsites']
BOOTSTRAP_THEME="flatly"
SHOW_ARTICLE_AUTHOR=True
SHOW_DATE_MODIFIED=True
DISQUS_SITENAME = "kamyanskiy"


# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('vk', 'https://vk.com'),
          ('Instagram', "https://instagram.com"),
          ('Facebook', 'https://facebook.com'),
          ('GitHub', 'https://github.com/kamyanskiy'),)

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = False
