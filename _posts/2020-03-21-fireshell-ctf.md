---
title: "Fireshell CTF 2020"
date: 2020-03-21 12:34:00 +0800
categories: [CTF, writeup]
tags: [favicon]
toc: true
---

## Introduction


> The FireShell CTF is a Brazilian event in jeopardy style. The proposal is to test participants' hacking skills in a challenging yet fun environment.


I participated with the team IrisCS and scored 1807 points landing us in 52nd Place. We completed 4 challenges. 


## Against the Perfect Discord Inquisitor 1

Information: 19 Solves, 495 Points.

```
You're on a journey and come to the Tavern of a Kingdom Enemy, you need to get information of a secret organization for the next quest. Be careful about the Inquisitor! He can ban you from this world.

TL;DR find the flag

Link to Challenge: https://discord.gg/fHHyU6g
```

See the Youtube Video below for my writeup.

[![ATPDI1](http://img.youtube.com/vi/-COfkwjVEyY/0.jpg)](http://www.youtube.com/watch?v=-COfkwjVEyY "ATPDI1")

## Miscrypto Alphabet

Information: 446 Points

```
points: 446
description: Help us to recover the alphabet.
```

As we can see from the image, we have a square for each letter of the alphabet as well as an interesting bar on the top of the image.

![AlphabetCrypto](/assets/problem_files/fireshell2020/alphabet.png)


The solution here is to create a matrix/system of equations for each of the pictured words. In total, we will get 26 equations to solve. 

For example, A is Apple. So, we will do 1A+2P+1L+E=453.

If we complete this calculation all the way through and solve (I used an online calculator after writing out my equations) we get the flag.

Flag:
> F#{y0u-ar4-gr34t-w1th-z3!}

## Welcome Challenge

```
Welcome to FireShell CTF 2020.

Follow us in our social networks:

Facebook Instagram Linkedin Telegram Twitter
```

On the Twitter Page, we find this image:

![TwitterAdvert](https://pbs.twimg.com/media/ETeXKWWXkAA7ZCH?format=jpg&name=large)

I scanned the QR Code with my phone and got the flag.

Flag:
> F#{Fr4ç01S3_d'4ub1gNé}
