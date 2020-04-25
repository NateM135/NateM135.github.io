---
title: "Biodiversity"
date: 2020-04-30 12:35:00 +0800
categories: [CS]
tags: [labs]
toc: true
---

> We are interested in how much biological diversity exists in line of cells. Each cell may either be alive (represented by
A) or dead (represented by D).


## Instructions

<a href="/assets/ths_senior/Biodiversity.pdf">View Instructions.</a><br>

Remember, if you are given a coding problem, the solution is probably HashSet ~Mr. Allen.

```
import java.util.*;

class Biodiversity
{
   public static int getDiversity(String lineOfCells)
   {
      Set<String>strands = new HashSet<String>();
      boolean inStrand = false;
      int countStrand = 0;
      for(int i = 0; i<lineOfCells.length(); i++)
      {
        if(countStrand == strands.size())
        {
          //return 1;
        }
        if(i ==0 && lineOfCells.charAt(0)=='A')
        {
          inStrand = true;
          countStrand++;
          System.out.println("first letter a");
          continue;
        }
        
        if(lineOfCells.charAt(i)=='D')
        {
          if(inStrand)
          {
            inStrand = false;
            strands.add("" + countStrand);
            countStrand = 0;
          }
        }
        else if(inStrand)
        {
          countStrand++;
        }
        else
        {
          inStrand = true;
          countStrand++;
        }
        
      }
      if(countStrand>0)
      {
        strands.add("" + countStrand);
      }
      return strands.size();
   }
}
```