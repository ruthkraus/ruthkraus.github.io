Title: Pelican plugin for Jupyter/IPython Notebooks
Category: Blog
Tags: notebook, jupyter

Today I read about nice thing that called as [Jupyter](http://jupyter.readthedocs.io)
I installed its locally, it's cool to play with python there and store results in 
files with .ipynb extension locally. 
Then I found that it is plugin [pelican-ipynb](https://github.com/danielfrg/pelican-ipynb)
for Pelican. With that plugin enabled, Pelican easy creates html pages with proper 
markup like into Jupyter. I'll try to use it sometimes, to avoid copying code samples
from **ipython** console to markdown files. Its possible to convert .ipynb content 
to nice formatted article !

So I created separate **plugins** folder in my site hierarchy and 
cloned repo [pelican-ipynb](https://github.com/danielfrg/pelican-ipynb) into
my **plugins** folder to ipynb directory.
```
 $ git clone https://github.com/danielfrg/pelican-ipynb ipynb

```

So my tree looks like 

```
plugins/
└── ipynb
    ├── core.py
    ├── __init__.py
    ├── ipynb.py
    ├── liquid.py
    ├── markup.py
...
```

In **pelicanconf.py** file I added "ipynb.markup" to PLUGINS list.  

```python
PLUGINS = ['i18n_subsites',
           'related_posts',
           "tag_cloud",
           "tipue_search",
           "ipynb.markup"
           ]
```
Then add 

```python
MARKUP = ('md', 'ipynb')
```

And added new plugins path

```
PLUGIN_PATHS = ['pelican-plugins/', 'plugins/']

```

That's all settings. In next article I'll try to use this plugin.

P.S. I had to fork ipynb repo and did little fix, to make date in metadata file
.ipynb-meta not mandatory. So now I use fork [pelican-ipynb](https://github.com/kamyanskiy/pelican-ipynb) 