---
title: "Fun with 2D arrays"
date: 2020-04-23 12:35:00 +0800
categories: [CS]
tags: [labs]
toc: true
---

## Introduction




<a href="/assets/ths_senior/2.FunWith2DArrays.pdf">View Instructions.</a><br>

Alternatively, see comments above each method for details about functionality. 

I completely stole one method from someone (ily nate c)


```
import java.lang.*;
import java.util.*;
import java.lang.Math;

 class FunWith2DArrays
{
/*
 *    preCondition : isArrow[i].length == isArrow[k].length for all i, k, 0 < i,j < isArrow.length
 *                   isArrow.length > 0  && isArrow[0].length > 0
 *
 *    postCondition: returns true if the 2D array is a square array (same number of rows and columns)
 *                           and the 2d array contains zeros in all entries except the first row,
 *                           first column and the main diagonal
 */
   public boolean isArrowHeadArray( int[] [] isArrow)
   {

      if(isArrow.length!=isArrow[0].length)
      {
        return false;
      }
      for(int r = 0; r<isArrow.length; r++)
      {
        for(int c = 0; c<isArrow.length; c++)
        {
          if(r!=c && r!=0 && c!=0)
          {
            if(isArrow[r][c]!=0)
            {
              return false;
            }
          }
          if(isArrow[0][c]==0 || isArrow[r][0]==0 || isArrow[r][r]==0 )
          {
            return false;
          }
          
        }
      
    }
    return true;
   }

/*
 *    preCondition  : gpa[j].length == gpa[k].length for 0 <= j, k < gpa.length
 *                   gpa.length > 0  && gpa[0].length > 0
 *
 *
 *    postcondition : returns true if mgp is as Generalized Permutation Matrix with integer entries
 *                    that is, returns true iff the following conditions are true
 *                      1)  All entries in the Matrix are integers
 *                             since you are being passed an int[][], you do not need to test this condition
 *                      2)  there is exactly one nonzero entry in each row and each column.
 *                          The nonzero entry can be any nonzero value (e.g., a positive or negative int)
 *                      3)  The array is a square array  (number of rows == number of columns)
 */
    public boolean isIntegerGeneralizedPermutationArray(int[][] gpa){
        int i,j;
        for(int r=0;r<gpa.length;r++){
            i=0;
            for(int c=0;c<gpa[0].length;c++){
                if(gpa[r][c]!=0)
                    i++;
                if(r==0){
                    j=0;
                    for(int rr=0;rr<gpa.length;rr++)
                        if(gpa[rr][c]!=0)
                            j++;
                    if(j!=1)
                        return false;
                }
            }
            if(i!=1)
                return false;
        }
        return true;
    }

/*
 *    preCondition : ma[i].length == ma[k].length for all i, k, 0 <= i,j < ma.length
 *                   ma.length > 0  && ma[0].length > 0
 *
 *                   Do NOT assume the 2d array is a square array
 *                   That is, ma.length may not be equal to ma[0].length 
 *
 *    postcondition : returns true if ma is a Monge Matrix
 *                    A m-by-n matrix is said to be a Monge array if for all i, j, k, p
 *                      with 0 <= i K k < m    and 0 <= j < p < n
 *                      and ma[i][j] + ma[k][p] <= ma[i][p] + ma[k][j]
 */
public boolean isMongeArray(int[][] ma){
  
   for(int i=0; i<ma.length; i++){
      for(int j=0; j<ma[i].length; j++){
         try{
            if( ma[i][j] + ma[i+1][j+1] > ma[i][j+1] + ma[i+1][j] ){
               return false;
            }
         }catch(Exception e){}
      }
   }
   return true;
   
}
}

```