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
#BOOTSTRAP_FLUID = True
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
PYGMENTS_STYLE = 'emacs'
DEFAULT_DATE = 'fs'

# Enable plugins
PLUGIN_PATHS = ['pelican-plugins/']
PLUGINS = ['i18n_subsites',
           'related_posts',
           "tag_cloud",
           "tipue_search",
           ]
# Tipue search
DIRECT_TEMPLATES = ('index', 'categories', 'authors', 'archives', 'search')

#https://github.com/getpelican/pelican-plugins/tree/master/related_posts
RELATED_POSTS_MAX = 5
#RELATED_POSTS_SKIP_SAME_CATEGORY = True

#https://github.com/getpelican/pelican-plugins/tree/master/tag_cloud
TAG_CLOUD_STEPS = 2
TAG_CLOUD_MAX_ITEMS = 20
TAG_CLOUD_SORTING = 'random'
TAG_CLOUD_BADGE = False
DISPLAY_TAGS_INLINE = True
DISPLAY_TAGS_ON_SIDEBAR = True


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

TYPOGRIFY = True

FILENAME_METADATA = '(?P<date>\d{4}\d{2}\d{2})-(?P<slug>.*)'
# Set URL's
TAG_URL = 'label/{slug}/'
TAG_SAVE_AS = 'label/{slug}/index.html'
TAGS_URL = 'label/'
TAGS_SAVE_AS = 'label/index.html'
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
CATEGORIES_URL = 'category/'
CATEGORIES_SAVE_AS = 'category/index.html'
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = ARTICLE_URL
AUTHORS_URL = ''
AUTHORS_SAVE_AS = ''
ARCHIVES_URL = 'archives/'
ARCHIVES_SAVE_AS = 'archives/index.html'
YEAR_ARCHIVE_URL = '{date:%Y}/'
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_URL = '{date:%Y}/{date:%m}/'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = PAGE_URL

ABOUT_ME = "<span>I love Python and happy to use it everyday for develop Web applications, writing tests and others cool things.</span>"
AVATAR = "images/profile.jpg"

FAVICON = SITELOGO

DISPLAY_BREADCRUMBS = True
DISPLAY_CATEGORY_IN_BREADCRUMBS = False

DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
RECENT_POST_COUNT = 5
#HIDE_SIDEBAR = True
#SIDEBAR_ON_LEFT = True
#DISABLE_SIDEBAR_TITLE_ICONS = False

# Add social share buttons https://www.addthis.com/dashboard#dashboard-analytics
ADDTHIS_PROFILE = 'ra-59403121442ae6be'
#DDTHIS_DATA_TRACK_ADDRESSBAR = True
#ADDTHIS_FACEBOOK_LIKE = True
#ADDTHIS_TWEET = True
#ADDTHIS_GOOGLE_PLUSONE = True

# Uncomment following line if you want document-relative URLs when developing
DELETE_OUTPUT_DIRECTORY = True
RELATIVE_URLS = False
