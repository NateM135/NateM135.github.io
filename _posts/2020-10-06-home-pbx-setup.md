---
title: "Home PBX Setup with VMWare/VirtualBox Tutorial"
date: 2020-10-06 16:00:00 -0700
categories: [tutorial, writeup]
tags: [writeup]
toc: true
---

## Introduction

Someone in the cybersecurity club made a VOIP system using a Pi and I thought that sounded interesting. I'm currently using my pi to host another project, so I decided to use a virtual machine for this project. 

By the end of this post, you will see how I set up a 3CX PBX that can make calls from my Desktop computer to my iPhone.

## Downloads

I'm going to be using a Debian 9 virtual machine along using VMWare. You can download the VM I am using [from this link](https://www.linuxvmimages.com/images/debian-9/). There's also a VirtualBox download link if you prefer to use it. 

If you use this VM, take note that the default login is ``debian:debian``.

## Networking Setup

The next thing we want to do is to get our virtual machine to get an IP address as if it was a normal device on my network. By this, I mean that we will configure this virtual machine to be a normal host that uses DHCP to get an address from my physical router. Here is how you would do it in VMWare. 

You should be doing this on the Debian VM you downloaded. I am doing it on a different virtual machine although the process is the same.

Click on your VM and click on ``Edit Virtual Machine Settings``. 

![NS1](https://i.imgur.com/NEVFFyB.png)

Click on Network Adapter and under the Network Connection section click ``Bridged``. Here is a screenshot of my settings:

![NS2](https://i.imgur.com/5iy62Ol.png)

Hit ``OK`` and you're good.

If you are using VirtualBox, click on the Debian VM you imported.

Hit Settings.

![NS3](https://i.imgur.com/coCchI6.png)

Go to Network and change your settings to look like this:

![NS4](https://i.imgur.com/Kevvzs2.png)

And you're done! Launch the VM and ensure you can connect to the internet.

## PBX VM Setup

At this stage, you should have a terminal open on a debian machine. 

The first thing we want to do is update everything on the machine. Use the following commands.

```
sudo apt-get update
sudo dpkg --configure -a
sudo apt-get -y upgrade
```

At this point, we want to make sure everything has updated and installed properly, so we will reboot the machine.

```
sudo reboot
```

Next, we want to add the 3CX package repositories to our system. Let's download the GPG key.

```
wget -O- http://downloads-global.3cx.com/downloads/3cxpbx/public.key | sudo apt-key add -
```

Next, we are going to add the package repository.

```
echo "deb http://downloads-global.3cx.com/downloads/debian stretch main" | sudo tee /etc/apt/sources.list.d/3cxpbx.list
```

Now we need to upgrade and install everything. Enter these commands. 

```
sudo apt update
sudo apt install -y net-tools dphys-swapfile
sudo apt -y install 3cxpbx
```

Once you go through that, you will see this screen: 

![Intitial_Screen](https://i.imgur.com/1iVXlBh.png)

Press ``tab`` and then press ``enter``.

![ConfigTool](https://i.imgur.com/73hcs47.png)

Type ``1`` and let it finish doing its thing. 

You will see this:

![FinishedConfig](https://i.imgur.com/b23kAlY.png)

This means everything has installed properly. You are given a link to access the web-console with. 

From the above screenshot, mine is ``http://192.168.1.222:5015/?v=2``. 

Awesome! At this point, it's important to understand that this web server and the PBX in general are running off of the virtual machine. If you close the virtual machine, suspend the virtual machine, or turn your host machine off, then the PBX will stop working as well.

## PBX Web Setup

I will now go to the webpage on my host machine (the machine running VMWare/VirtualBox). Once you do, you are greeted with this page: 

![WebSetup1](https://i.imgur.com/R4jK0Vu.png)

For clarification, this is the link that I was given after installing everything on the virtual machine. 

Let's get a license key. I entered a fake phone number and my spam email address. Here is what I put into the registration fields:

![LK](https://i.imgur.com/49hSmTV.png)

After that, you will get a verification email. Once your account is verified, you will be emailed some credentials in this format:

```
Customer Portal URL: https://customer.3cx.com/
Username: natem135spam@googlemail.com
Password: U6VJj55tEZ88
```

Click the verification link and the URL will be in this format:

```
https://customer.3cx.com/prm/pbxexpress.aspx?provider=OnPremise&licensekey=K7RQ-OF2B-BPHQ-U63C
```

At the end, you will find your license key. Enter that back into the IP you were at earlier. 

You now have the option to set your username/password. For simplicity, I went with ``admin:Adminadmin99!``.

It will show your Public IP. Yes, that is your IP. 

On the next screen, choose ``Dynamic IP``.

On the next screen, you will need to select the Subdomain/FQDN.

So, for the name I will use ``natem135``. 

Domain Group I will choose ``United States``. 

Preferred Domain Suffix I will choose California ``ca.3cx.us``. 

On the next set of settings, I will leave all of the defaults.

For reference, here are the default settings:

```
5001 - HTTPS
5000 - HTTP
5060 - SIP
5090 - Tunnel Port
```

Now, for the next setting, I will choose to use my local IP instead of the domain name I set up above. You can use either one. This is the setting I have (you can reference it with settings above)

```
192.168.1.222 ens33 (ens33)
```

Hit next, and then let it set up what it needs to. This process took around 5 minutes for me to complete.

## Configure the PBX

Now that everything has been setup, we can start to configure the PBX. The first setting we have is the ``Extension Length``. An extension is a shorter number you will use with your PBX to call another user. I will use a four digit extension. 

Next is an ``admin email``. I used my spam email account for this.

Next is your country and timezone which were configured earlier so they should be autocompleted already.

After that you have to create an operator extension. I chose to use ``6666``. with the name ``O. P.`` and the email ``op@test.com``. 

The next is countries that you can make calls to. I chose North America for obvious reasons. 

Then you can select your language. I chose English.

Now that all that is done, you are put onto a page with two links. One is your domain name from earlier and the other is your public ip with the https port appended onto it. You can use either of these to configure your PBX when you are not at your house or connected to your LAN. 

It also tells you your admin credentials again.

Now, let's go to the same IP address from earlier (the one from the debian VM) and let's connect using HTTPS and Port 5001. 

Username: admin

Password: Adminadmin99!

```
https://192.168.1.222:5001/
```

![lpkek](https://i.imgur.com/rnBsfQI.png)

Awesome! Let's login using the credentials we made. 

We are now given a prompt to install the 3CX App and scan a QR code. This associates the phone with the PBX. 

On the app go to:

Settings -> Accounts -> + Button

Now the Operator's name and extension are listed on the mobile app. 

Next, we want to go Extensions -> Add. Add an extension, and you can enter the minimal amount of settings shown below:

![s1](https://i.imgur.com/Ovx07fG.png)

Now hit "OK". 

Click on the extension you just made and scan that number with the mobile app like we did above. It should now show your name and the extension we associated with it. 

You can verify that it has been added correctly using the ``Phones`` tab. Here is mine:

![s2](https://i.imgur.com/Svl05WB.png)

Awesome! Now let's add my computer as a second device. I am running Windows, so I will download the Windows client here: https://www.3cx.com/phone-system/3cxphone/

Add a new extension and this time add an email address. As soon as you finish making the extension, the email address will be sent a ``Welcome Email``. In this email, a config file is attatched. Download it and "drag" it onto the Desktop application. Once you do that, you will see your extension and the other extension listed. 

Now you're done! On the Desktop client, click on the other extension and hit call. If you did everything correctly to this point, you should recieve a call on your phone!


