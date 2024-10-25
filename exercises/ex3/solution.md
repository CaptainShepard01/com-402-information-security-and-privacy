# COM-402 Cookie Tampering, HMAC and Authentication Solution

- [Exercise 1: Cookie tampering](#exercise-1-cookie-tampering)
  - [The initial problem](#the-initial-problem)
  - [So, where are the cookies?](#so-where-are-the-cookies)
  - [Decode and understand the cookie](#decode-and-understand-the-cookie)
  - [Haxxxing the cookie](#haxxxing-the-cookie)
- [Exercise 2: HMAC for cookies](#exercise-2-hmac-for-cookies)
  - [HMAC ?](#hmac-)
  - [Create the cookie](#create-the-cookie)
  - [Login the user](#login-the-user)
  - [Checking a cookie](#checking-a-cookie)
  - [Authenticating the user](#authenticating-the-user)
- [Exercise 3: Client-Side Password Verification](#exercise-3-client-side-password-verification)
  - [Understanding the setup](#understanding-the-setup)
  - [Ew, Javascript](#ew-javascript)
  - [Some explanations](#some-explanations)
  - [Hacking](#hacking)

## Exercise 1: Cookie tampering
### The initial problem
The title already gives a lot of information on how you should proceed. Have a look at your [cookies](https://www.wikihow.com/View-Cookies) for now. Without doing nothing, there is nothing of interest here (to check that, you can open the URL in a private navigation window, that starts clean of cookies). Nothing to tamper with yet...

Open your browser console (right-click -> inspect is a good way), and open the _Network_ tab. When clicking on the "Hack & Spy" buttons, you see a request made to `api/ex1/list`. The request headers don't contain something of interest. The response is a `403 Forbidden`.

\[Optional\] You can also inspect the HTML of the page, and notice, at the very bottom a `<script>` tag, that contains the code that binds the button to HTTP requests to `api/ex1/list`, with an empty payload, and that deals with the result of the request (display the success or mock you when you fail).

### So, where are the cookies?

When you arrive on the webpage, the first things to spot is the possible interactions. Obviously, the "Hack & Spy" buttons, but also the hyperlink on the word _administrators_, which leads you to `/ex1/login.html`, and a nice login form. That's nice!

Enter some credentials (can be any dummy value, like `myusername` and `mypassword`). You're now back to the homepage, and still can't _hack & spy_ :( But, going back to your cookies, you now have a cookie!

| name        | value                 | domain    | Expires |
| ---------   | :-------------------: | -------   | ------- |
| LoginCookie | `bXl1c2VybmFtZS...`   | localhost | Session |

### Decode and understand the cookie

The value (that will vary for you) is quite gibberish though... But as a trained IT security expert, you immediately recognize base64! If you don't, here are a few tips:
* A long string of alphanumerical characters is most likely base64
* If it ends by one or several `=` characters, it also is.
* base64 is [very common](https://en.wikipedia.org/wiki/Base64#URL_applications) on the web and in cookies, to encode arbitrary text or content.
* There are [tools](https://www.webatic.com/encoding-explorer) online to help with that

You can use the `base64` tool from GNU coreutils for encoding/decoding into base64 format. You can also use online tools like [base64decode.org](https://base64decode.org). Input the cookie value, and you'll obtain something along the lines of `myusername,1594232326,com402,hw3,ex1,user`. You can try multiple times (go to the login page, and enter credentials again), and you will notice that:
* The first value (`myusername`) is always your username
* The second value changes each time, but slightly (this is a good indicator of a [timestamp](https://www.unixtimestamp.com/))
* The next 3 values never ever change.

The interesting thing about base64 is that it is completely and deterministically reversible. This means that you can change anything in that string, and re-encode it at will.

Try again to _Hack & Spy_, nothing changes. But now, you see in the request headers that the cookie is sent along. This means, your login information also is. Maybe we can **tamper** with that. The last (decoded) value of the cookie is `user`. Maybe we can try to change it?

### Haxxxing the cookie

Modify the cookie decoded value, and modify the characters you are interested in. At this point, you don't know the "roles" in the page, except `user`. There are many keywords you can try, such as `root`, `editor`, `owner`, `administrator`, `admin`,... We'll settle for the latter! Change `user` by `admin`,  (to obtain something like `myusername,1594232326,com402,hw3,ex1,admin`), and encode.

Now go to your browser again, modify your cookie with the newly encoded string, and now you can _Hack & Spy_!

## Exercise 2: HMAC for cookies
We are again having fun with cookies. It's now time to be on the other side, and be smarter than Evil Corp.

### HMAC ?
First of all, it's important to remember what a [HMAC](https://en.wikipedia.org/wiki/HMAC) is. Basically, you store on your server a _secret key_ (some arbitrary string, only known to you, a _one-time pad_). Then, when you need to ensure integrity of a content, you xor the content with your key, hash it, and append it to the content. With that, if someone wants to tamper with the content, they must also modify the HMAC (which they can't, because they don't have the secret).

### Create the cookie
First step, we need a function to create the cookie. As mentioned, we need the username and password to determine if a user is an admin, then we create the cookie, compute its HMAC and append it. Here is a snippet that does that:

```python
import time # for the timestamp
import hmac # standard lib for the HMAC
from hashlib import sha1 # hashing library to provide to hmac
import base64 # encode/decode base64 strings

# your secret key
SECRET_KEY_YOU_WILL_NEVER_FIND = "ducks".encode()

def create_cookie(username, password):
    # the infos required for the cookie
    t = str(int(time.time())) # create the timestamp
    domain = "com402"
    hw = "hw3"
    ex = "ex2"

    # decide the role based on the username/password
    if username == "admin" and password == "42":
        role = "admin"
    else:
        role = "user"

    # create the "base" cookie, that will be hashed
    base_cookie = ",".join([username,t,domain,hw,ex,role])

    #create the HMAC
    my_hmac = hmac.new(SECRET_KEY_YOU_WILL_NEVER_FIND,
                   base_cookie.encode(), #message must be binary
                   sha1)
    final_cookie = base_cookie + "," + my_hmac.hexdigest() # append digest
    # base64encode the cookie (with .encode() for binary format),
    # then back to utf-8 for a readable cookie
    return base64.b64encode(final_cookie.encode()).decode('utf-8')
```
Note a few specialties there:
* The `hmac` library works with binary values, this is why we have to use `.encode()` on the secret key and the base cookie, to change them from utf-8 strings to binary strings.
* We used here sha1, which is a rather standard hashing algorithm, but other  (md5, sha2,...) can be used.
* base64 also works with binary values: we first encode `final_cookie` to binary, then change it to base64 (which yields a result in binary), then decode it again to utf-8 for a usable format.
* The method used to authenticate the admins is absolutely terrible, never apply that in real life. This is purely a demonstration.
* Same apply for the secret key, you should use a longer and more random one.

### Login the user
Now that we have a way to create the cookie, we can login the user. We reuse the template that was provided, and complete the `/login` route.

```python
from flask import Flask, make_response, request

@app.route("/login", methods=["POST"]) # only accept POST
def login():
    # get the username/password from the payload
    username = request.form.get('username')
    password = request.form.get("password")
    ####
    # [optional] here, you can perform sanity checks
    # (are they both non-null, etc.)
    ####
    # create your cookie
    c = create_cookie(username, password)
    # prepare your response (the text is useless)
    resp = make_response("Logged in")
    # set the cookie with the correct cookie name
    resp.set_cookie(cookie_name, c)
    # return your response
    return resp
```
Nothing too crazy here: get the values from the POST request, create your cookie, prepare a response, set the cookie and send it.

You can already test that in your lab. Do a POST request, and then check the session cookies. You should see the cookie, with the base64-encoded value (that you can decode as in ex1, to ensure it's correct)

### Checking a cookie
Now that the user has a cookie, we must build a function that, provided the cookie, will answer if the cookie is legit. We will first take the cookie, base64decode it, put aside the HMAC, re-compute it, and compare them.

```python
def cookie_validate(cookie):
    try: # optional: try to decode, but don't trust too much
        decoded = base64.b64decode(cookie.encode()).decode("utf-8")
    except:
        # The cookie isn't even a base64 encoding anymore,
        # it definitely has been tampered with...
        return False
    # separate base cookie from hmac
    base_cookie, cookie_hmac = decoded.rsplit(",", 1)
    # re-compute the hmac from the base cookie
    reference_hmac = hmac.new(SECRET_KEY_YOU_WILL_NEVER_FIND,
                     base_cookie.encode(),
                     sha1).hexdigest()

    # return whether or not they are equal
    return cookie_hmac == reference_hmac
```

### Authenticating the user
Now that we can ensure the cookie is valid, we can do the complete authentication step.
```python
@app.route("/auth",methods=['GET'])
def auth():
    # get the LoginCookie from the cookie jar
    cookie = request.cookies.get(cookie_name)
    if cookie is None or not cookie_validate(cookie):
        # no cookie found, or not valid
        return "Naughty, naughty, naughty...", 403
    # decode the cookie
    decoded = base64.b64decode(cookie.encode()).decode("utf-8")
    # get the role
    role = decoded.split(",")[5]
    # compare and return the correct code
    if role == "admin":
        return "My lord...", 200
    return "User", 201
```

See `server.py` for the complete solution. Cli client invokation.

```
$ curl --cookie-jar /tmp/cookie -d 'username=u&password=p' -X POST http://localhost:5000/login
Logged in⏎
$ cat /tmp/cookie
# Netscape HTTP Cookie File
# https://curl.se/docs/http-cookies.html
# This file was generated by libcurl! Edit at your own risk.

localhost	FALSE	/	FALSE	0	LoginCookie	dSwxNzI3MDM0MTEwLGNvbTQwMixodzMsZXgyLHVzZXIsODg5NGU2N2RmZDUxYmYwMDZiMTA1YTM2NDJiN2I3YmJhZjA3NzM2MA==
$ echo dSwxNzI3MDM0MDY3LGNvbTQwMixodzMsZXgyLHVzZXIsYmFkMDZmZTU1NTE5NTVjZjk0ZTI3NjdkZjM1Y2YwZjcxNTMyNDJmYQ== | base64 -d
u,1727034067,com402,hw3,ex2,user,bad06fe5551955cf94e2767df35cf0f7153242fa⏎
curl http://localhost:5001/auth
Naughty, naughty, naughty...⏎
$ curl -b /tmp/cookie http://localhost:5000/auth
User⏎
```

## Exercise 3: Client-Side Password Verification

As you may suspect, this exercise will focus on the verification of a password without actually sending the password to the server, and letting the user do the work.

### Understanding the setup
When you arrive on the login screen, first thing first, open the browser console, on the Network tab. Then fill in any dummy data, and login. Strangely, no request was made to the server. Interesting! It looks like _client-side password verification_. So where does the error message come from ? Surely from some javascript method.

### Ew, Javascript
Now, before you pull out the debugger and understand the process, have a look at the HTML. At the very bottom, as previously, you have a `<script>` tag that contains all the interesting code. Here is a copy, for convenience:

```javascript
function ascii (a) { return a.charCodeAt(0); }
function toChar(i) { return String.fromCharCode(i); }

function hash(msg,key) {
    if (key.length < msg.length) {
        var diff = msg.length - key.length;
        key += key.substring(0,diff);
    }

    var amsg = msg.split("").map(ascii);
    var akey = key.substring(0,msg.length).split("").map(ascii);
    return btoa(amsg.map(function(v,i) {
        return v ^ akey[i];
    }).map(toChar).join(""));
}

$('#loginForm').submit(function(e) {
    e.preventDefault();
    var mySecureOneTimePad = "Never send a human to do a machine's job";
    var username = $('#username').val();
    var password = $('#password').val();

    if (username.length > 100) {
        alert("There's a difference between knowing the path and walking the path.");
        return;
    } else if (password.length > 100) {
        alert("The best answer to anger is silence.");
        return;
    }
    if (password != hash(username,mySecureOneTimePad)) {
        alert("I didn't say it would be easy, Neo. I just said it would be the truth.");
        return;
    }
    postJSON = function(url,data){
        return $.ajax({url:url, data:JSON.stringify(data), type:'POST', contentType:'application/json'});
    };
    postJSON("/api/ex3",{"username":username,"password":password})
        .done(function(data) {
        //if you get a 200 OK status, that means you successfully
        // completed the challenge.
        document.write("Sucess! Token: " + data);
    }).fail(function(resp,status) {
        alert("Pain is temporary. Quitting lasts forever.");
    });
});
```

### Some explanations
We won't go into too much details there, because not everything is relevant. But the interesting parts to notice are the following:
* There is a function `hash` that takes a message and a key, and apparently returns some hash,
* The submit action of the submit button is intercepted and replaced by the big block,
* This block defines a OTP, and retrieves the username/password from the form,
* It checks the length of both of them,
* Then compare the password to the resulting hash of the username and the OTP,
* Then, if it matches, it sends the username and password to the server for a second check.

The second check is necessary to ensure we don't bypass the function entirely and simply send the username/password ourselves. So it's either the exact same mechanism (but server-side), or a different one.

### Hacking
The weakness of this client-side verification, is that it relies on a HMAC but gives out the OTP, that is supposed to be secret. It then simple to guess a password: input any username and the OTP into the hash function (both kindly provided), and use the output as a password!

You don't even need to understand how the hash function works. Simply use it as a blackbox. Go to the javascript console (the _console_ tab of your browser console), then copy the OTP, and input it with some username to the hash function (already defined):
```javascript
> let otp = "Never send a human to do a machine's job";
> hash("myusername", otp)
"IxwDFhdSHQQDAQ=="
```

Go now to the form, and input `myusername` and `IxwDFhdSHQQDAQ==`, granting you access!

### Reference and Credits
- https://bntan.medium.com/understanding-oath-hotp-authentications-42dc6012c41d
- https://bntan.medium.com/understanding-oath-totp-authentications-ed95b002a6e3
- https://datatracker.ietf.org/doc/html/rfc2104
- https://datatracker.ietf.org/doc/html/rfc4226
- https://datatracker.ietf.org/doc/html/rfc6238

