## Welcome to GitHub Pages

You can use the [editor on GitHub](https://github.com/kamyanskiy/kamyanskiy.github.io/edit/master/README.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/kamyanskiy/kamyanskiy.github.io/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.

### Start development server

```shell
$ pelican -rl
```

### Install tipue_search 
```shell
python -m pip install -e "git+https://github.com/getpelican/pelican-plugins/#egg=pelican-tipue-search&subdirectory=tipue_search"
```


### Get updates from fork origin
```shell
git remote add upstream connection-url
git pull upstream master
git push origin master
```

### Push changes to github
```shell
pelican content -o output -s pelicanconf.py
ghp-import output -b master
git push git@github.com:kamyanskiy/kamyanskiy.github.io.git master:master 
```
