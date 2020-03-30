---
title: "001 Venn Diagram"
date: 2020-03-30 12:34:00 +0800
categories: [CS]
tags: [labs]
toc: true
---

## Introduction


> Venn Diagram. Complete each of the methods according to name and comments.


```
import java.lang.*;
import java.util.*;
import java.lang.Math;
/**
 * @author  Don Allen
 */
class VennDiagram
{
    int[] numbers;
    
    public VennDiagram(int[] n)
    {
        numbers = n;
    }

    /*
     *   @return the number of values in numbers that are divisible by 2
     */
    public int numDivisibleBy2()
    {
      int ans = 0;
      for(int i = 0; i<numbers.length; i++)
      {
        if(numbers[i]%2==0)
        {
          ans++;
        }
      }

        return ans;
    }

    /*
     *   @return the number of values in numbers that are divisible by 3
     */
    public int numDivisibleBy3()
    {
      int ans = 0;
      for(int i = 0; i<numbers.length; i++)
      {
        if(numbers[i]%3==0)
        {
          ans++;
        }
      }

        return ans;
    }

    
    /*
     *   @return the number of values in numbers that are greater than 50
     */
    public int numGreaterThan50()
    {
      int ans = 0;
      for(int i = 0; i<numbers.length; i++)
      {
        if(numbers[i]>50)
        {
          ans++;
        }
      }

        return ans;
    }

    /*
     *   @return the number of values in numbers that are
     *            divisible by 2 and divisible by 3
     */
    public int numDivisibleBy2AndDivisibleBy3()
    {
        int ans = 0;
        for(int i = 0; i<numbers.length; i++)
        {
          if(numbers[i]%2==0 && numbers[i]%3==0)
          {
            ans++;
          }
        
        }
        
        return ans;
    }

    /*
     *   @return the number of values in numbers that are
     *            divisible by 2 and greater than 50
     */
    public int numDivisibleBy2AndGreaterThan50()
    {

        int ans = 0;
        for(int i = 0; i<numbers.length; i++)
        {
          if(numbers[i]%2==0 && numbers[i]>50)
          {
            ans++;
          }
        
        }
        
        return ans;
    }

    /*
     *   @return the number of values in numbers that are
     *            divisible by 3 and greater than 50
     */
    public int numDivisibleBy3AndGreaterThan50()
    {
        int ans = 0;
        for(int i = 0; i<numbers.length; i++)
        {
          if(numbers[i]%3==0 && numbers[i]>50)
          {
            ans++;
          }
        
        }
        
        return ans;
    }

    /*
     *   @return the number of values in numbers that are
     *            divisible by 2, divisible by 3 and greater than 50
     */
    public int numDivisibleBy2AndDivisibleby3AndGreaterThan50()
    {

        int ans = 0;
        for(int i = 0; i<numbers.length; i++)
        {
          if(numbers[i]%2==0 &&numbers[i]%3==0 && numbers[i]>50)
          {
            ans++;
          }
        
        }
        
        return ans;
    }
}
```