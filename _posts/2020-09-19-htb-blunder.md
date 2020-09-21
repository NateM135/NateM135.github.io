---
title: "HTB Blunder"
date: 2020-09-19 12:35:00 +0800
categories: [HTB, writeup]
tags: [writeup]
toc: true
---

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

We now have credentials, epic. Now that we have admin credentials, we can make use of the second vulernability: https://www.cvedetails.com/cve/CVE-2019-16113/

In short, with these credentials, RCE is possible.










