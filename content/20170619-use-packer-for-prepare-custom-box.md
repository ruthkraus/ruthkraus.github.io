Title: Use Packer to prepare custom Vagrant box
Category: Blog
Tags: vagrant, packer, vagrant-vbguest

What is Packer?

Packer is an open source tool for creating identical machine images for multiple 
platforms from a single source configuration. Packer is lightweight, runs on
every major operating system, and is highly performant, creating machine images
for multiple platforms in parallel. Packer does not replace configuration 
management like Chef or Puppet. In fact, when building images, Packer is able
to use tools like Chef or Puppet to install software onto the image.

A machine image is a single static unit that contains a pre-configured operating
system and installed software which is used to quickly create new running 
machines. Machine image formats change for each platform. Some examples include
AMIs for EC2, VMDK/VMX files for VMware, OVF exports for VirtualBox, etc.

[Packer documentation](https://www.packer.io/docs/index.html)

Here I want to write down how to use template file to prepare my own box from
one of base boxes from [https://atlas.hashicorp.com](https://atlas.hashicorp.com/boxes/search) site.
It's maybe not usual approach, I want just to play with Packer, their arguments, etc.
I think probably in real life it's enough to use Vagrantfile with one of provision 
methods. But here I want to learn how to create my own box from existing base box
with Packer.

I decided to use **hashicorp/precise64** box, so first I init box 

```commandline
vagrant init hashicorp/precise64
``` 

Then I know that box can be found by path $HOME/.vagrant/boxes/hashicorp-VAGRANTSLASH-precise64/1.1.0/virtualbox/box.ovf
So I want to create my own box with 1Gb RAM, 2 CPU based on initial 
**hashicorp/precise64** box. I want to provision machine with bash script that 
 installs some additional packages, then I want to get my own box as artifact and 
 upload it to my atlas storage.
 
Script **bootstrap.sh** that I want to ask to Packer to run during provisioning\
looks like:

```commandline
#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y apache2
if ! [ -L /var/www ]; then
  sudo rm -rf /var/www
  sudo ln -fs /vagrant /var/www
fi
sudo apt-get install -y mc
sudo apt-get install -y htop
sudo apt-get install -y postgresql-9.1 postgresql-server-dev-9.1 libpq-dev python-dev python-setuptools
sudo apt-get clean

```

Template file called as **packer.json** :

```json
{
  "variables": {
    "home": "{{env `USERPROFILE`}}"
  },
  "builders": [{
    "type": "virtualbox-ovf",
    "source_path": "{{ user `home` }}/.vagrant.d/boxes/hashicorp-VAGRANTSLASH-precise64/1.1.0/virtualbox/box.ovf",
    "ssh_username": "vagrant",
    "ssh_password": "vagrant",
    "ssh_wait_timeout": "30s",
    "guest_additions_mode": "disable",
    "shutdown_command": "echo 'packer' | sudo -S shutdown -P now",
    "vboxmanage": [
    ["modifyvm", "{{.Name}}", "--memory", "1024"],
    ["modifyvm", "{{.Name}}", "--cpus", "2"]]
  }],
  "provisioners": [{
    "type": "shell",
    "script": "bootstrap.sh",
    "pause_before": "30s"
  }],
  "post-processors": [{
    "type": "vagrant",
    "keep_input_artifact": true,
    "output": "box/modified-hashicorp-VAGRANTSLASH-precise64.box"
  },
  {
  "type": "atlas",
  "artifact": "kamyanskiy/precise64",
  "artifact_type": "vagrant.box",
  "metadata": {
    "provider": "virtualbox",
    "version": "1.0.0"
  }
  }
]
}

```

The one thing, to upload artifact to atlas via 'atlas' post-processor, I have to
create ATLAS_TOKEN and set it to my environment variables.

![atlas_token]({static}/images/atlas_token.png)


To start Packer to build

```commandline
packer build packer.json
```

After that Virtualbox manager will be shown and process logged into console:

![packer1]({static}/images/packer_progress.png)

![packer2]({static}/images/packer_vbox.png)

When build succeed, I can see my uploaded box in my [vagrant boxes](https://atlas.hashicorp.com/vagrant) list.

The one thing, if I upload box via atlas post-processor, this box is uploaded 
to the not free area and I need to pay money to use it, there Atlas gave me trial 1 month 
period. I removed box that I played with, but I still can use box that Packer created
"box/modified-hashicorp-VAGRANTSLASH-precise64.box"

```commandline
vagrant box add mybox modified-hashicorp-VAGRANTSLASH-precise64.box
cd ../mybox
vagrant init mybox
vagrant up
```

So probably the way, when I create box manually on [Vagrant site](https://atlas.hashicorp.com/vagrant)
is more preferable for me now, it is free, but yes it requires some additional 
manual work. It's not so cool like auto create by **atlas** post-processor.

#### Keep VirtualBOX additions fresh

I found that almost all Ubuntu images that I used to play with, have old VirtualBox 
addition pack. It's very useful plugin to keep always Vbox additions fresh version.

The next command installs **vagrant-vbguest** on machine and every **vagrant up**
command at the end it checks if Vbox additions are freshest and updates it if that 
is necessary.

```commandline
vagrant plugin install vagrant-vbguest
```
