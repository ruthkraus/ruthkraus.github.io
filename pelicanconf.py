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
SHOW_ARTICLE_AUTHOR = True
SHOW_DATE_MODIFIED = True

# Show my last activity on GitHub
GITHUB_USER = 'kamyanskiy'

# Enable custom theme
THEME = "pelican-themes/pelican-bootstrap3/"
BOOTSTRAP_THEME = "flatly"
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
PYGMENTS_STYLE = 'emacs'
DEFAULT_DATE = 'fs'

# Enable plugins
PLUGIN_PATHS = ['pelican-plugins/']
PLUGINS = ['i18n_subsites']

# Enable disqus comments
DISQUS_SITENAME = "kamyanskiy"

SITELOGO = 'images/logo.png'

STATIC_PATHS = ['images', 'extra/custom.css']
CUSTOM_CSS = 'theme/css/custom.css'

EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': 'theme/css/custom.css'}
}

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('Django', 'https://https://docs.djangoproject.com/'),
         ('Flask', 'http://flask.pocoo.org/'),
         )

# Social widget
SOCIAL = (('vk', 'https://vk.com/id216671695'),
          ('Facebook', 'https://www.facebook.com/alexander.kamyanskiy'),
          ('GitHub', 'https://github.com/kamyanskiy'),)

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
DELETE_OUTPUT_DIRECTORY = True
TYPOGRIFY = True
