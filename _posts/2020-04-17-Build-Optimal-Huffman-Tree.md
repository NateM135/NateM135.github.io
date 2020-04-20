---
title: "BuildOptimalHuffmanTree"
date: 2020-04-17 12:35:00 +0800
categories: [CS]
tags: [labs]
toc: true
---

## Introduction

Complete the implementation of the BuildOptimalHuffmanTree class per directions in the file attached with the assignment posted in Google Classroom.

That is, first complete the constructor, getFrequuencyTable() methods

and complete the getOptimalTree() method.

Class HuffmanNode is include and does NOT need to be changed. You are welcome to add additional helper methods as described n the file attached with the assignment posted in Google Classroom.


<a href="/assets/ths_senior/Huffmancode_Part1.pdf">View Instructions.</a><br>

Alternatively, see comments. 


```
import java.lang.*;
import java.util.*;
import java.lang.Math;
/**
 * @author  Don Allen
 */
 class BuildOptimalHuffmanTree
{
    private Map<String, Integer>  letterFrequenceMap;

/*
 *   No two chars in letters will have the same getFrequency
 *
 */
public BuildOptimalHuffmanTree(String letters)
{
    letterFrequenceMap = new HashMap<String,Integer>();
    for(char c:letters.toCharArray())
    {
        if(letterFrequenceMap.get(""+c)!=null)
        {
            letterFrequenceMap.put(""+c,letterFrequenceMap.get(""+c)+1);
        }
        else
        {
            letterFrequenceMap.put(""+c,1);
        }
    }
}

    /*
     */
    public Map<String, Integer> getFrequencyTable()
    {
        return letterFrequenceMap;
    }

    public HuffmanNode getOptimalTree(){
      Map<Integer,String> map = new HashMap<Integer,String>();
      for(String s:letterFrequenceMap.keySet())
          map.put(letterFrequenceMap.get(s),s);
      List<HuffmanNode> list = new ArrayList<HuffmanNode>();
      while(map.keySet().size()>0)
      {
          int min = Collections.min(map.keySet());
          list.add(new HuffmanNode(map.get(min),null,null,min));
          map.remove(min);
      }
      while(list.size()>1){
          HuffmanNode min = list.remove(0);
          HuffmanNode mun = list.remove(0);
          int f = min.getFrequency() + mun.getFrequency();
          HuffmanNode com = new HuffmanNode("",min,mun,f);
          if(list.size()==0)
          {
              return com;
          }
          int x = 0;
          while(list.get(x).getFrequency()<f)
          {
              x++;
              if(x==list.size())
              {
                  break;
              }
          }
          list.add(x,com);
      }
      return null;
  }
}





/**
 * Write a description of class HuffmanNode here.
 *
 * @author (your name)
 * @version (a version number or a date)
 */
class HuffmanNode
{
    // instance variables
    private String str;
    private HuffmanNode left;
    private HuffmanNode right;
    private int freq;

    /**
     * Constructor for objects of class HuffmanNode
     */
    public HuffmanNode(String s, HuffmanNode l, HuffmanNode r, int f)
    {
       str = s;
       left = l;
       right = r;
       freq = f;
    }

    public HuffmanNode getLeft()
    {
        return left;
    }

    public HuffmanNode getRight()
    {
        return right;
    }

    public String getValue()
    {
        return str;
    }

    public int getFrequency()
    {
        return freq;
    }

    public void setFrequency(int f)
    {
        freq = f;
    }
}

```