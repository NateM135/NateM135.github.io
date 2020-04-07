---
title: "Forest Playground"
date: 2020-04-07 12:34:00 +0800
categories: [CS]
tags: [labs]
toc: true
---

## Introduction


<a href="/assets/ths_senior/04_Forest_Playground.pdf">View Instructions.</a><br>

Alternatively, see comments. 


```
import java.io.*;
import java.util.*;
import java.math.*;
import java.lang.*;
import java.lang.Math;
/**
 * @author  Don Allen
 */
class ForestPlayGround 
{
    String[] myTree;

    /*
     *   PreConditions
     *        tree is a valid represntation fo a binary tree
     *        tree != null
     *        tree.size() >= 0
     */
    public ForestPlayGround(String[] tree)
    {
        myTree = tree;
    }

    /*
     *    return the number of non null nodes in myTree
     */
    public int getNumNodes()
    {
        int numNodes = 0;
        for(int i = 0; i<myTree.length; i++)
        {
          if(myTree[i]!=null)
          {
            numNodes++;
          }
        }

        return numNodes;
    }

    /*
     *    A leaf is a node in the tree in which both children have 0 children.
     *    An empty tree contains NO leafs
     */
    public int getNumLeafs()
    {

      
      int numLeafs = 0;
      int left, right, counter;
      
      for(int i = 1; i<myTree.length; i++)
      {
        if(myTree[i]==null)
        {
          continue;
        }
        
        System.out.println(i);
        counter = 0;
        left = (2*i)+1;
        right = (2*i)+2;
        if(left>myTree.length-1)
        {
          counter++;
        }
        else if(myTree[left]==null)
        {
          counter++;
        }
        if(right>myTree.length-1)
        {
          counter++;
        }
        else if(myTree[right]==null)
        {
          counter++;
            
        }
        if(counter==2)
        {
          numLeafs++;
        }
        
      }

      return numLeafs;
    }

    /*
     *    Precondition:   0 <= p < myTree.length
     *
     *    returns:
     *        the right child of myTree[p]
     *        null if myTree[p] does not have a right child
     */
    public String getRightChild(int p)
    {
      int right = (2*p)+2; 
      if(right<=myTree.length-1)
        {
          if(myTree[right]==null)
          {
            return null;
          }
          else
          {
            return myTree[right];
          }
           
        }
      return null;
      
        
    }

    /*
     *    Precondition:   0 <= p < myTree.length
     *
     *    returns:
     *        the left child of myTree[p]
     *        null if myTree[p] does not have a left child
     */
    public String getLeftChild(int p)
    {
      int left = (2*p)+1; 
      if(left<=myTree.length-1)
        {
          if(myTree[left]==null)
          {
            return null;
          }
          else
          {
            return myTree[left];
          }
           
        }
      return null;
    }

    /*
     *    Precondition:   0 <= p < myTree.length
     *                    myTree[p] != null
     *
     *    returns:
     *        the parent of myTree[p]
     *        null if myTree[p] does not have a parent
     */
    public String getParent(int p)
    {
      if(p==0)
      {
        return null;
      }
      
      int parent = (p-1)/2; 
      if(parent>=0)
        {
          if(myTree[parent]==null)
          {
            return null;
          }
          else
          {
            return myTree[parent];
          }
           
        }
      return null;
    }
    
    public int getIndexOfParent(int p)
    {
      int parent = (p-1)/2; 
      return parent;
    }
    public int getIndexOfLeft(int p)
    {
      int left = (2*p)+1;  
      return left;
    }
        public int getIndexOfRight(int p)
    {
      int right = (2*p)+2; 
      return right;
    }


    /*
     *    Precondition:   0 <= p < myTree.length
     *                    myTree[p] != null
     *
     *    returns:
     *        the List of all ancestors (parent and their parent ans so on) of myTree[p]
     *        an empty List if myTree[p] does not have a parent
     */
    public List<String> getAncestors(int p)
    {
        
        List<String> ans = new ArrayList<String>();
        int temp = getIndexOfParent(p);
        while(temp>=1)
        {
          ans.add(myTree[temp]);
          temp = getIndexOfParent(temp);
          
        }
        if(myTree[0]!=null && (myTree[1]!=null || myTree[2]!=null))
        {
          ans.add(myTree[0]);
        }
        
        return ans;
    }

    /*
     * Preconditions:
     *    myTree[p] != null
     *    0 <= p < myTree.length
     */
    public List<String> getDescendants(int p){
        List<String> ans = new ArrayList<String>();
        if(getLeftChild(p)!=null){
            ans.add(getLeftChild(p));
            for(String str: getDescendants(2*p+1))
                ans.add(str);
        }
        if(getRightChild(p)!=null){
            ans.add(getRightChild(p));
            for(String str: getDescendants(2*p+2))
                ans.add(str);
        }
        return ans;
    }

    /*
     *    In a complete binary tree every level, except possibly the last, is completely filled,
     *    and all nodes in the last level are as far left as possible.
     *    
     *    This implies that the end of the array may contain multiple nulls
     *                               and the array/tree may still be complete
     */
public boolean isComplete()
{
    boolean foundNull = false;
    for(String s:myTree)
    {
        if(s==null)
        {
            foundNull=true;
        }
        else if(foundNull)
        {
            return false;
        }
    
  }
  return true;
  }

    /*
     *    A full binary tree is a tree in which every node in the tree has either 0 or 2 children.
     */
    public boolean isFull()
     {
  
    if(myTree.length==0)
    {
      return true;
    }

    for(int i = 0; i<myTree.length; i++)
    {
      if(getRightChild(i)!=null && getLeftChild(i)!=null)
      {
        continue;
      }
      else if(getRightChild(i)==null && getLeftChild(i)==null)
      {
        continue;
      }
      else
      {
        return false;
      }
      
    }
    return true;
  }
}
```