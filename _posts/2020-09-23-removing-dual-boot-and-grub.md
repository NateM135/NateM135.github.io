---
title: "Removing Dual Boot and Grub"
date: 2020-09-23 12:35:00 +0800
categories: [tutorial]
tags: [linux]
toc: true
---

## Introduction

When I started using linux-based operating systems, I wanted to try and use them for daily tasks in everyday life. Unfortunately, I still needed Windows while at school for certain classes so I was unable to use Ubuntu 24/7. As a result, I had a dual boot setup where my computer would boot into grub, the linux bootloader, and I could choose whether to launch ubuntu or windows. 

Now that I'm heading into college, I decided to go full Ubuntu. Thus, I needed to repartition my existing Ubuntu installation and remove my Windows installation. I eventually decided to reinstall Ubuntu all-together for simplicity, so in this little "writeup" I'll show how I removed my dual-boot incase I end up needing to know how to do this in the future.

## Step 1: Deleting the Linux Partition

The first thing you need to do is to boot into Windows and open the disk management tool. Find the partition where your linux installation is (it will be labeled as the "primary" partition) and right click -> delete it.

## Step 2: Removing Grub
At this point, you have deleted the linux partition but you have not deleted grub, or the boot loader. If you restart your computer now, you will be thrown into a grub shell. In order to fix this, we want to remove grub from our machine. Here's how you do it:

1) Open a command prompt with administrator privledges.

2) Type ``diskpart``. This is a command-line utility that allows us to manage drives.

3) Type: ``list disk`` then ``sel disk X`` where X is the drive your boot files reside on. For me, this is my main Windows partition.

4) Type ``list vol`` to see all partitions (volumes) on the disk (the EFI volume will be formatted in FAT, others will be NTFS)

5) Select the EFI volume by typing: ``sel vol Y`` where Y is the SYSTEM volume. (We will need to access this to remove the last traces of grub)

6) Assign a drive letter by typing: ``assign letter=Z:`` where Z is a free (unused) drive letter. You can use any letter, just replace the letter Z with the letter you decided to use in step 8.

7) Type ``exit`` to leave disk part

8) Type: ``Z:`` (or whatever you chose in step 6) and hit enter.

9) Type ``dir`` to list directories on this mounted EFI partition If you are in the right place, you should see a directory called EFI.

10) Type ``cd EFI`` and then dir to list the child directories inside EFI.

11) Type ``rmdir /S ubuntu`` to delete the ubuntu boot directory

Assuming you only ever had two operating systems (Win 10 & Ubuntu) you should now be able to boot directly to Windows without hitting the black grub screen. This is because the only bootloader left is the Windows Bootloader.

If this does not work, check out this thread for additional answers, suggestions, and troubleshooting help: https://askubuntu.com/questions/429610/uninstall-grub-and-use-windows-bootloader.

## Step 3: Restart!

If you did everything correctly, you should now be able to boot directly to Windows without hitting the grub shell. This is because the only bootloader left is the Windows Bootloader.

















