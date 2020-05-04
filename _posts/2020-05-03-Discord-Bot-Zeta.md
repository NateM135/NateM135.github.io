---
title: "Zeta Notifications - Helper for WaifuBot"
date: 2020-05-03 12:35:00 +0800
categories: [CS]
tags: [labs]
toc: true
---

![WaifuBot Banner](https://remilia.cirno.pw/banner.png)

# Zeta Notifications for WaifuBot

[![BotInvite](https://img.shields.io/badge/Invite%20bot-Click%20here-ff69b4.svg "Invite the bot to your server")](https://bit.ly/ZetaNotifs) [![ServerInvite](https://img.shields.io/badge/Join%20Test%20Server-Click%20here-success.svg "This is where you can test the bot")](https://discord.gg/3YM9cPq)

**As of now I will be hosting the bot. Invite it with the button above. If I am unable to host it in the future, I will update this README.**

This bot was created by in order to notify users when a high-rarity waifu is spawned by WaifuBot. Additionally, the bot lists the rarity of each Waifu that spawns.


When a Zeta/pink waifu spawns, this bot will mention a user, role, or ping specified by the owner of the server.

### Server Setup)


To set the person who will be notified when a Zeta spawns, use 

```
z!setping <ping>
```
 
The ping can be a role, a single user, or @everyone/@here.

### Examples

###### User

![userexample](https://i.imgur.com/niN2LQS.png)

###### Roles

The first thing you should do is create a role with this permission enabled:

![roleex1](https://i.imgur.com/TE5ymww.png)

After that, you can use the z!setping command again.

![roleex2](https://i.imgur.com/flvw5gG.png)

###### Other Pings

```
z!setrole @everyone
```

```
z!setrole @here
```

**In order to ping more than one user you need to create a role!**

### Normal Spawns

The bot will comment on the rarity of all the spawns in each server it is in. Below are a few examples.

![spawn1](https://i.imgur.com/16yutUB.png)
![spawn2](https://i.imgur.com/wfB2t2y.png)
![spawn3](https://i.imgur.com/kvJS9Ji.png)
![spawn4](https://i.imgur.com/VttWjDC.png)

### Zeta Spawns

This is what the bot will look like when a Zeta is spawned.

![zetasamplespawn](https://i.imgur.com/VGiiv0q.png)

### Self Hosting the Bot

This bot is made with discord.py, so we will need to set up an environment to run the bot in.

This guide assumes that you already have Python3 installed on your PC. If you do not have Python3 installed, install it first before proceeding.

Open your common prompt and type the following:

```
pip3 install -r .\requirements.txt
```


If you are on Windows, you need to run the command prompt as administrator. If you are on Linux, add sudo before the command.


Next, open 

```
setup.py
```

and place your bot token into the file.



Here is what it looks before you add a token:

```
#Enter Your bot token here inbetween the single quotes.
TOK = ''
```

Here is what it should look like AFTER you add a token:
```
#Enter Your bot token here inbetween the single quotes.
TOK = '6qrZcUqja7812RVdnEKjpzOL4CvHBFG'
```

**Note, tokens difer in length. Yours may not be as long as mine. For instructions on how to get your bot's token, [click here](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)


Now that you have your token set up, you are ready to run the bot. Go back to your command prompt and type:

```
python3 .\bot.py 
```

This will begin the bot. If everything has worked, your command prompt will have something similar to the following prompt:

```
We have logged in as Zeta Notifications#3432
```

In this case, Zeta Notifications#3432 is the public verison of the bot that I am hosting on my VPS. Your user will be different if you are self hosting.

At this point, you can generate an oauth link and follow the server setup instructions above!



