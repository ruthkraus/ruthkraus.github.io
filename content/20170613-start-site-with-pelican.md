Title: Start blog site on GitHub pages with Pelican
Category: Blog

One day I found that I forgot many things I learned and used before, so I 
decided to make short memos about different
programming aspects, issues and new tools I'll learn and touch in the future.    

#### Create GitHub user page
GitHub provides easy and nice possibility to create your own site with
 [User Pages](https://pages.github.com/) 
So as described in this [tutoral](https://pages.github.com/) I've created repo 
with special name 
[kamyanskiy.github.io](https://github.com/kamyanskiy/kamyanskiy.github.io)
The content from **master** branch from this repo should be used to display on 
access [https://kamyanskiy.github.io](https://kamyanskiy.github.io) url.

#### Create site with Pelican
I found that possibility that provided from GitHub to have static pages with
 [jekyll](https://help.github.com/articles/using-jekyll-as-a-static-site-generator-with-github-pages/) is nice, but 
[Pelican](http://docs.getpelican.com) is more powerful tool, with rich number
 of plugins and nice themes.
So I checkout my [kamyanskiy.github.io](https://github.com/kamyanskiy/kamyanskiy.github.io) 
repository from branch **master** to **pelican** branch and start to install Pelican.
 
 1. Install Pelican.

```
$ virtualenv -p python3.6 .env
$ source .env/bin/activate
(.env) $ pip install pelican markdown 
```

2. Get [pelican-plugins](https://github.com/getpelican/pelican-plugins/tree/f3b5cef79d97556cb1c10e66e9130a223f45c943) 
and [pelican-themes](https://github.com/kamyanskiy/pelican-themes/tree/012591f2e625674bd02961f1f29dbe9fc40940f4) submodules
After review many nice themes on site [http://www.pelicanthemes.com/](http://www.pelicanthemes.com/) 
I've decided to use [pelican-bootstrap3](https://github.com/getpelican/pelican-themes/tree/master/pelican-bootstrap3) theme,
with little changes, so I've forked [pelican-themes](https://github.com/getpelican/pelican-themes) 
repo to make custom changes. 

```
$ git submodule add git@github.com:getpelican/pelican-plugins.git pelican-plugins
$ git submodule add https://github.com/kamyanskiy/pelican-themes pelican-themes

```

3. Create simple site template 
Once Pelican has been installed, you can create a skeleton project via the
 **pelican-quickstart** command,
which begins by asking some questions about your site.
 
```
 pelican-quickstart
```
Then answer to questions or keep just all defaults, it's possible to change
 all later, manually in file **pelicanconf.py**
 
4. Configure **pelicanconf.py**
The all possible settings are described in 
[documentation](http://docs.getpelican.com/en/3.6.3/settings.html)
My settings file looks like:
 
```python
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
RELATIVE_URLS = False
DELETE_OUTPUT_DIRECTORY = True
TYPOGRIFY = True
```

5. Add some content 
I've added this page in .md format into content/20170613-start-site-with-pelican.md file

6. Use Fabric to manage site
It's possible to use fabric utility to make some useful things with site content,
 like run dev server and push changes to GitHub pages
I've used Fabric3 to use with python3.6 on my machine

**Install Fabric3**
```
$ pip install fabric3 ghp-import 
```
**Fix **fabfile.py** (for usage with python3)**
 Change 
 ```
 import SocketServer 
 ```
 to 
 ```
 import socketserver
 ```
 
To use fab command to start dev server , run
```
$ fab serve
```
To publish content to master branch on github repo, run
```
$ fab gh_pages
```

7. TODO: Add info how to enable DISQUS comments