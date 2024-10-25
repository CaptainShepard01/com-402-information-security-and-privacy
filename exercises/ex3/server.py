import base64
import hmac
import time
from hashlib import sha1

from flask import Flask, request, make_response

app = Flask(__name__)

cookie_name = "LoginCookie"


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


if __name__ == '__main__':
    app.run()
