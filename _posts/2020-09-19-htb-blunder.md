---
title: "HTB Blunder"
date: 2020-09-19 12:35:00 +0800
categories: [HTB, writeup]
tags: [writeup]
toc: true
---

## Introduction

HTB Blunder is the first box where I managed to solve both the user flag and the root flag, so consider this to be a celebratory writeup! In the past, all of my writeups have been for small CTF challenges that can be solved within 4-5 minutes max, so writing up something as long as a full HTB challenge is definetely new to me. I am experimenting a bit in terms of categorization, although I hope the quality doesn't suffer too much. If this guide is helpful, great, glad it helped you! If it sucked, let me know how I can make it better. I am not the best when it comes to writing well and I'm using CTFs/HTB as a way to increase my writing skills.

With that out of the way, this is my guide for the challenge ``Blunder``. It took me around 5 hours to get the user flag, and it took me 15 minutes to get the root flag from there (very popular exploit was used.)

## Enumeration

As usual with HTB, the first thing to do is to use nmap to scan the box. The IP of the box is ``10.10.10.191``, as you can see in the command I used:

``nmap 