---
title: "Leetcode Practice 11/4"
date: 2020-11-04 13:45:00 -0700
categories: [leetcode]
tags: [cpp]
toc: true
---

> Leetcode Practice 11/4/2020

## 1108. Defanging an IP Address


> Given a valid (IPv4) IP address, return a defanged version of that IP address. A defanged IP address replaces every period "." with "[.]"


https://leetcode.com/problems/defanging-an-ip-address/

```
class Solution {
public:
    string defangIPaddr(string address) {
        string ans = "";
        for(int i = 0; i<address.size(); i++) {
            if(address.at(i)=='.') {
                ans = ans + "[.]";
            }
            else {
                ans = ans + address.at(i);
            }
        }
        return ans;
        
    }
}
```

## Jewels and Stones

https://leetcode.com/problems/jewels-and-stones/

> You're given strings J representing the types of stones that are jewels, and S representing the stones you have.  Each character in S is a type of stone you have.  You want to know how many of the stones you have are also jewels. The letters in J are guaranteed distinct, and all characters in J and S are letters. Letters are case sensitive, so "a" is considered a different type of stone from "A".

```
class Solution {
public:
    int numJewelsInStones(string J, string S) {
        int count = 0;
        for(int i = 0; i<J.size(); i++) {
            for(int j = 0; j<S.size(); j++) {
                if(J.at(i)==S.at(j)) {
                    count++;
                }
            }
        }
        return count;
    }
};
```
## 1342. Number of Steps to Reduce a Number to Zero

https://leetcode.com/problems/number-of-steps-to-reduce-a-number-to-zero/

> Given a non-negative integer num, return the number of steps to reduce it to zero. If the current number is even, you have to divide it by 2, otherwise, you have to subtract 1 from it.

```
class Solution {
public:
    int numberOfSteps (int num) {
        int steps = 0;
        while(num!=0) {
            if(num%2==0) {
                num = num/2;
                steps++;
            }
            else {
                num -=1;
                steps++;
            }
        }
        return steps;
        
    }
};
```

