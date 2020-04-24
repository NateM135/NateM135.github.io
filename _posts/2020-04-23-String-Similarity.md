---
title: "String Similarity"
date: 2020-04-23 12:36:00 +0800
categories: [CS]
tags: [labs]
toc: true
---

## Introduction

> see instructions in Google Classroom

I have attatched the instruction document below.


<a href="/assets/ths_senior/0.String_Similarity.pdf">View Instructions.</a><br>

Alternatively, see comments above each method for details about functionality. 

```
import java.lang.*;
import java.util.*;
import java.lang.Math;


// Nathan Melwani
//string are immutable in my heart


 class StringSimilarity
{
/*
 *    postCondition : return a list with list.get(i).length() == 1 for all i, 0 <= i < list.size()
 *                            All elements of list are contained in String s1 or String s2
 *                            Duplicate elements may exist in list if s1 or s2 contain duplicate elements
 */
   public static List<String> stringUnion( String s1, String s2 )
   {
      List<String> ans = new ArrayList<String>();
      String string2 = s2;
      for(int i = 0; i<s1.length(); i++)
      {
        String temp = "" + s1.charAt(i);
        ans.add(temp);
        string2 = string2.replaceFirst(temp, "");
      }
      
      for(int i = 0; i<string2.length(); i++)
      {
        String temp = "" + string2.charAt(i);
        ans.add(temp);        
      }
      return ans;
   }


/*
 *    postCondition : return a list with list.get(i).length() == 1 for all i, 0 <= i < list.size()
 *                            All elements of list are contained in both String s1 and String s2
 *                            Duplicate elements may exist in list if both s1 and s2 contain duplicate elements
 */
   public static List<String> stringIntersection( String s1, String s2 )
   {
      List<String> ans = new ArrayList<String>();
      String string1 = s1;
      String string2 = s2;
      for(int i = 0; i<s1.length(); i++)
      {
        String temp = "" + s1.charAt(i);
        if(string2.contains(temp))
        {
          ans.add(temp);
          string1 = string1.replaceFirst(temp, "");
          string2 = string2.replaceFirst(temp, "");
        }
      }
      return ans;
   }

   public static double getJaccardIndex(String s1, String s2)
   {
     if(stringIntersection(s1, s2).size() == 0 && stringUnion(s1, s2).size() == 0)
     {
       return 1.0;
     }
     return (double)( stringIntersection(s1, s2).size() ) / (double)(stringUnion(s1, s2).size());
   }
}
```