import sys, subprocess, os
import urllib.request, http, ssl, urllib, time
import requests
import requests.packages.urllib3 as urllib3

requests.packages.urllib3.disable_warnings()


def check_https(url, check_CA):
    print("Checking https on", url)
    try:
        f = None
        if not check_CA:
            context = ssl._create_unverified_context()
            f = urllib.request.urlopen(url, context=context).read().decode()
        else:
            f = requests.get(url, verify="/app/rootCA.pem").text

        print("Received content:\n{}".format(f))
        print("HTTPS is enabled, CA was {}verified".format("" if check_CA else "NOT "))
        return

    except requests.exceptions.SSLError as e:
        print("Error: Certificate was not signed by CA.")
        print(e)
    except http.client.RemoteDisconnected:
        print("Error: Couldn't connect.")
    except ssl.SSLError as e:
        print("Error: Certificate error")
        print(e)
    except ssl.SSLEOFError as e:
        print("Couldn't start SSL", e)
    except urllib.error.URLError as e:
        print("Couldn't start SSL - URL error", e)

    print("Test failed.")
    sys.exit(1)


time.sleep(2)

print("\n------ TEST PART A : HTTP ------")

r = requests.get("http://server", allow_redirects=False)
if r.status_code == 200 or 301:
    if r.status_code == 200:
        print("Successfully made a simple HTTP request")
        print("Part A: Success!")
    else:
        print("I'm seeing a HTTPS redirect. If you're doing part B or C, that's normal")
        print("Part A somewhat successful")
else:
    print("Unable to do a simple request, failed")
    sys.exit(1)
print("\n------ TEST PART B : SELF-SIGNED CERTIFICATE ------")

if not "https" in r.headers["Location"]:
    print("Your server not redirecting to HTTPS.")
    print("Test failed.")
    sys.exit(1)


check_https("https://server", False)
print("Part B: Success!")

print("\n------ TEST PART C1: Signed certificate ------")
check_https("https://server", True)


print("\n------ TEST PART C2: HSTS ------")
check_https("https://server", True)
r = requests.get("https://server", allow_redirects=False, verify=False)
if not "Strict-Transport-Security" in r.headers:
    print("Your server does not set the header Strict-Transport-Security.")
    print("Test failed.")
    sys.exit(1)
else:
    print("HSTS successfully enabled")

print("Tests succeeded!")
sys.exit(0)
