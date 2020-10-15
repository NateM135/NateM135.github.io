---
title: "THM OhSINT"
date: 2020-10-15 16:00:00 -0700
categories: [THM, writeup]
tags: [writeup, osint]
toc: true
---

> TryHackMe OhSINT: What information can you possible get with just one photo?

## Introduction

TryHackMe's OhSINT is a beginner open source intelligence (OSINT) challenge.

It took around 20 minutes to solve this challenge.

We are given the following picture and seven different questions to solve.

![avatar](https://i.imgur.com/h20DaaQ.png)

## Question 1: What is this users avatar of?

Alright, we have a WindowsXP background image. First things first, let's look at the metadata of the file.

According to wikipedia, metadata is ``the data providing information about one or more aspects of the data; it is used to summarize basic information about data which can make tracking and working with specific data easier.``

In simpler terms, say you take a picture on your phone and you go back to look at it. Your phone tells you what place you took the picture at and when you took the picture. This information is the metadata of the image. There is a cli tool called ``exiftool`` that will extract this metadata for us. Let's use it.

```
kali@kali:~/Desktop/thm/ohsint$ exiftool WindowsXP.jpg 
ExifTool Version Number         : 12.04
File Name                       : WindowsXP.jpg
Directory                       : .
File Size                       : 229 kB
File Modification Date/Time     : 2020:10:15 18:21:56-04:00
File Access Date/Time           : 2020:10:15 18:23:51-04:00
File Inode Change Date/Time     : 2020:10:15 18:23:39-04:00
File Permissions                : rw-r--r--
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
XMP Toolkit                     : Image::ExifTool 11.27
GPS Latitude                    : 54 deg 17' 41.27" N
GPS Longitude                   : 2 deg 15' 1.33" W
Copyright                       : OWoodflint
Image Width                     : 1920
Image Height                    : 1080
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 1920x1080
Megapixels                      : 2.1
GPS Latitude Ref                : North
GPS Longitude Ref               : West
GPS Position                    : 54 deg 17' 41.27" N, 2 deg 15' 1.33" W
```

There's two key things to take from this. We have a GPS location for where the picture was taken and a copyright information field which can lead to more details about who took the image. Let's search ``OWoodflint`` on google. The first result is a twitter page, let's open it: 

![twitter](https://i.imgur.com/A3ZkFaT.png)

Looks like he has an avatar of a cat and he is followed by ``Dark``, who is a TryHackMe admin. Seems like we are in the right place. 

The answer to the first question is what the user's avatar is, so the answer would be ``cat``. 

## Question 2: What city is this person in?

We get the location ``7PVX+WV Hawes, United Kingdom`` from the GPS data gained from the metadata, which is incorrect according to TryHackMe. Interesting, let's keep looking for more things. I put the twitter handle into google and found his github repo: https://github.com/OWoodfl1nt/people_finder

```
people_finder

Hi all, I am from London, I like taking photos and open source projects.

Follow me on twitter: @OWoodflint

This project is a new social network for taking photos in your home town.

Project starting soon! Email me if you want to help out: OWoodflint@gmail.com
```

Look's like he is in London, and TryHackMe accepts this answer.

``London``

## Question 3: Whats the SSID of the WAP he connected to?

This question is probably the hardest in this challenge and it is the one I solved last. 

On the twitter page from question 2, there are no tweets/responses to tweets. I found this interesting so I decided to use the wayback machine to see if he had tweets at one point. 

Here is a picture of what the account was like in December 2019:

![bruh](https://i.imgur.com/DNr10bd.png)

We are given a ``bssid`` and we have to find the SSID from this information. For reference, the bssid is like the MAC address of the router. There are websites where you can reverse search a bssid and get information about the network associated with it as all BSSIDs are unique. 

We want to use this website to reverse search it: https://wigle.net/

We run a basic search using the BSSID: 

![search](https://i.imgur.com/pqLHTm6.png)

``UnileverWifi`` is the SSID as shown in the results.


## Question 4: What is his personal email address?

Returning to the github repository from Question 2: https://github.com/OWoodfl1nt/people_finder

This is the README for the repo:

```
people_finder

Hi all, I am from London, I like taking photos and open source projects.

Follow me on twitter: @OWoodflint

This project is a new social network for taking photos in your home town.

Project starting soon! Email me if you want to help out: OWoodflint@gmail.com
```

``OWoodflint@gmail.com``

## Question 5: What site did you find this email address on?

Returning to the github repository from Question 2 and 4:: https://github.com/OWoodfl1nt/people_finder

This is the README for the repo:

```
people_finder

Hi all, I am from London, I like taking photos and open source projects.

Follow me on twitter: @OWoodflint

This project is a new social network for taking photos in your home town.

Project starting soon! Email me if you want to help out: OWoodflint@gmail.com
```

The website we found this on is:

``github``

## Question 6: Where has he gone on holiday?

Another search result that came up is this blog: https://oliverwoodflint.wordpress.com/author/owoodflint/

The only post is:

```
Author: owoodflint
Hey

Im in New York right now, so I will update this site right away with new photos!
```

``New York``. 


## Question 7: What is this persons password?

Loooking at the source code of the blog, we find this one interesting section:

```
<p>Im in New York right now, so I will update this site right away with new photos!</p>



<p style="color:#ffffff;" class="has-text-color">pennYDr0pper.!</p>
	</div><!-- .entry-content -->
```

Looks like this isn't even hidden, just colored so it wouldn't be seen... here's a screenshot of how the page looks:

![b4](https://i.imgur.com/EsN2CEE.png)

Now let's press ``ctrl+a``. 

![after](https://i.imgur.com/bNlbebU.png)

``pennYDr0pper.!`` is a hidden string in this context.

I tried submitting it as the password answer and it was correct ;o.

``pennYDr0pper.!``.

## Conclusion

This is a nice, simple beginner OSINT challenge that anyone should be able to solve. 

The tools/technologies I used are ``Google Dorks``, ``Wigle``, and the ``Wayback Machine``. These are all common tools that you will utilize frequently with OSINT challenges in competitions like the National Cyber League.

