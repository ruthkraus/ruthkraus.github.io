Title: How to add DISQUS comments to Pelican site
Category: Blog
Tags: Disqus, Pelican, Python

It is possible to attach [DISQUS](https://disqus.com) comments to blog site.

#### Setup your DISQUS Account 
Before you can use the commenting stuff, you need to register into Disqus. 
There you find a lot of disqus documentation that you simply not need :-) . 
Pelican already has done that for you.
  
1. Register on [DISQUS](https://disqus.com) site

1. Select 'I don't see my platform listed, install manually with Universal Code. 
![disqus1]({static}/images/disqus/disqus_1.png)

1. Remember 'Shortname'=kamyanskiy, it will be used later in site configuration. Fill fields Website name and Website URL.
![disqus2]({static}/images/disqus/disqus_2.png)

1. Check 'Allow guests to comments' 
![disqus3]({static}/images/disqus/disqus_3.png)

1. Finish settings with Add trusted site, my own is kamyanskiy.github.io 
![disqus4]({static}/images/disqus/disqus_4.png)

1. Into **pelicanconf.py** file enable DISQUS, just add these settings:
```pythonstub
DISQUS_SITENAME = "kamyanskiy"
```
Remember, here should be added 'shortname' from step 3.

That's done, now generate content and check that comments working fine:

![disqus5]({static}/images/disqus/disqus_5.png)