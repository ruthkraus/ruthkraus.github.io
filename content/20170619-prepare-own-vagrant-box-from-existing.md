Title: Create Vagrant base box manually from existing one
Category: Blog
Tags: vagrant, packer

Vagrant Boxes are prepackaged development environments that are provided by 
Vagrant. In most cases, this is usually just a stripped and naked operating 
system such as Ubuntu, Debian, or CentOS. Boxes exist with the intention to be 
provisioned with additional features like Apache server or PostgreSQL database  
with Puppet, shell script or anyone of provision tools. 

The main documentation about Vagrant configuration can be found [here](https://www.vagrantup.com/docs/index.html)

This post will describe how to create your own prepackaged Vagrant Box manually
from an existing box from https://atlas.hashicorp.com. In my opinion, it's the 
quickest and easiest way to save time for provisioning default box with Vagrant.
We need to provision machine manually once and then use it in the future, of course 
we can lost flexibility of usual Vagrant approach when I need always run provision
process for clean box. This way you'll be able to reuse prepared box over and 
over and even share it. 

For example I want to prepare my own box from existing Ubuntu box, many of
boxes could be found on [https://atlas.hashicorp.com](https://atlas.hashicorp.com/boxes/search) site.
I think for my purposes I get **hashicorp/precise64** , so I init it:

```commandline

vagrant init hashicorp/precise64

``` 

then I need to run it:

```commandline
vagrant up
```

after couple minutes I can enter machine via ssh and start to install things 
that I think I want to have in my own box:

```commandline
vagrant ssh
```

then do some commands to install mc, postgresql, etc :
 
```commandline
sudo apt-get update
sudo apt-get install -y apache2

sudo apt-get install -y mc
sudo apt-get install -y htop
sudo apt-get install -y postgresql-9.1 postgresql-server-dev-9.1 libpq-dev python-dev python-setuptools
sudo apt-get clean

```

All packages that I want already installed, now I can package that instance to my own 
box:

```commandline
vagrant package --output mynew.box
vagrant box add mynewbox mynew.box
vagrant destroy
vagrant init mynewbox

```

after that I can run my own box: 

```commandline
vagrant up
```

I can also upload that box up to atlas storage [kamyanskiy/ubuntu14_psql93](https://atlas.hashicorp.com/kamyanskiy/boxes/ubuntu14_psql93)
For that there I need to configure provider, version, upload image and then 
release it.
