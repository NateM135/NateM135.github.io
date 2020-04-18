---
title: "BuildOptimalHuffmanTree"
date: 2020-04-17 12:35:00 +0800
categories: [CS]
tags: [labs]
toc: true
---

## Introduction


<a href="/assets/ths_senior/Huffmancode_Part1.pdf">View Instructions.</a><br>

Alternatively, see comments. 


```
import java.lang.*;
import java.util.*;
import java.lang.Math;
/**
 * @author  Don Allen
 */
class HuffmanCodeWithArray
{
    private static String[] letterTree = new String[69];

    public HuffmanCodeWithArray(String[] myTree)
    {
        letterTree = myTree;
    }

    /*
     * remember:  0 goes left (lousy .... 
     *            1 goes right :)
     *            a space in message correspnds to a space in the return value
     *   @return 
     */
    public String getHuffmanMessage(String message)
    {
        String ans = "";
        int currentIndex = 1;
        for(int i = 0; i<message.length(); i++)
        {
          if(message.charAt(i)==' ')
          {
            ans = ans + " ";
            currentIndex = 1;
            continue;
          }
          if(message.charAt(i)=='0')
          {
            currentIndex = currentIndex*2;
            System.out.println(currentIndex);
          }
          else
          {
            currentIndex = currentIndex*2+1;
            System.out.println(currentIndex);
          }
          
          
          if(letterTree[currentIndex]!=null)
          {
            ans = ans + letterTree[currentIndex];
            currentIndex = 1;
          } 
          
        }
        return ans;
    }
}
```