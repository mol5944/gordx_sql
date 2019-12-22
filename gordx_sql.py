import requests
from bs4 import BeautifulSoup
from re import split,search
from urllib.parse import unquote
from sys import argv
from threading import Thread
from time import sleep
from termcolor import colored

errors = ['mysql_fetch_array()','mysql_num_rows()','MySQL','Database error','SQL syntax','MariaDB','SELECT * FROM']

def help():
    print('--wordlist (List of words with dorks)')
    print('--threads (Specify the number of threads)')
    print('--output (Output file)')
    print('--timeout (Waiting between requests)')
    quit()

def generator(string):
    for word in string:
        dork_check = word.replace('\n','')
        yield dork_check

def save_url(file_name,url):
    with open(file_name,'at') as file:
        file.write(url+'\n')

def get_url(dork):
    urls = list()
    url = "https://google.com/search?sxsrf=ACYBGNQchZe55s8cn9kLBA8Fr-k8ddYVLw%3A1576957731958&ei=I3f-Xd_8OYbk-gS-8LfoBQ&q=" + dork + "&oq=" + dork + "&gs_l=psy-ab.3..0i67j0i203j0i67j0i203l2j0i67j0i203l2j0i67j0i203.64062.64979..68671...0.5..1.546.2186.3-2j2j1......0....1..gws-wiz.......0i71j35i39j0j0i10.HZ2AvkT-AlQ&ved=0ahUKEwifmsGrwcfmAhUGsp4KHT74DV0Q4dUDCAs&uact=5"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,'html.parser')
    for i in soup.find_all('div',class_="kCrYT"):
        try:
            urls.append(split('&',unquote(split('=',i.a.get('href'),maxsplit=1)[1]))[0])
        except:
            pass
    return urls

def request(url,timeout):
    try:
        resp = requests.get(url + '\'',timeout=timeout)
        for error in errors:
            if search(error,resp.text) != None:
                print(url)
            
                if output != False:
                    save_url(output,url)

                break
            else:
                continue
    except:
        pass

def check(dork,timeout):
    for url in get_url(dork):
        request(url,timeout)


if '--help' in argv:
    help()

if '--wordlist' in argv:
    wordlist = argv[argv.index('--wordlist') + 1]
else:
    help()

if '--threads' in argv:
    threads = int(argv[argv.index('--threads') + 1])
else:
    threads = 10

if '--output' in argv:
    output = argv[argv.index('--output') + 1]
else:
    output = False

if '--timeout' in argv:
    timeout = int(argv[argv.index('--timeout') + 1])
else:
    timeout = 10

count = 0

with open(wordlist,'rt',errors='ignore') as dictionary:
    for dork in generator(dictionary):
        print(colored('Use: ' + dork,'green'))
        if count >= threads:
            sleep(10)
            count = 0

        thr = Thread(target=check,args=(dork,timeout,))
        thr.start()

        count += 1
