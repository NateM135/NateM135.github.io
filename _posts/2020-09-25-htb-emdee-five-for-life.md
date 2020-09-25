---
title: "HTB Challenge: Emdee Five for Life"
date: 2020-09-25 14:35:00 +0800
categories: [htb]
tags: [writeup, web, htb_chal]
toc: true
---

## Challenge Description

[20 Points] Emdee five for life [by L4mpje]

Can you encrypt fast enough?

## Writeup

![login](/assets/htb-emm-dee-5/site.png)

You are given a string that you have to md5hash. Unfortunately, once you put the hash in, it appears that it will always be too slow.

Because of this, let's try to script the hashing process using python and then send a post request as soon as we get the page.

```
import requests
import hashlib

link = "http://docker.hackthebox.eu:30338/"

r = requests.session()
init = r.get(link)
hash = hashlib.md5(init.text[167:].split("</h3>")[0].encode()).hexdigest()
print(hash)
data = {'hash': hash}
out = r.post(url=link, data=data)
print(out.text)
```

We need to use a session because we need to send an answer for the same question that we get before processing any data. Once we get the webpage contents using requests.get, I get the text that needs to be hashed using a starting point (because the starting point is the same each time) as well as split to truncate the rest of the response. After that, the string is hashed using hashlib and the string is printed in a readable form using ``hexdigest()``. After that, we craft a post request using the paramters seen in the source code of the webpage and print the response.

Now we run the script:

```
<html>
<head>
<title>emdee five for life</title>
</head>
<body style="background-color:powderblue;">
<h1 align='center'>MD5 encrypt this string</h1><h3 align='center'>GQzYFzfCW4JoB4xR1L0M</h3><p align='center'>HTB{N1c3_ScrIpt1nG_B0i!}</p><center><form action="" method="post">
<input type="text" name="hash" placeholder="MD5" align='center'></input>
</br>
<input type="submit" value="Submit"></input>
</form></center>
</body>
</html>
```

Flag: ``HTB{N1c3_ScrIpt1nG_B0i!}``

<a id="raw-url" href="natem135.github.io/assets/htb-emm-dee-5/sol.py">Click this link to download the script.</a>






