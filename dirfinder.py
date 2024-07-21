import requests
from queue import Queue
import threading
from tqdm import tqdm
from colorama import Fore, Back, Style
import argparse
import random
from requests.exceptions import ProxyError, RequestException

ad = Queue()
pr = []
parser = argparse.ArgumentParser(description="Multithreaded URL Checker")
parser.add_argument("-u", type=str, help="Base URL to check")  # Corrected type=str
parser.add_argument("-w", default="wordlist.txt",type=str, help="use external wordlist wordlist")  
parser.add_argument("-p", default="wordlist.txt",type=str, help="use proxy with search") 

args = parser.parse_args()

url = args.u
word = args.w
proxyword = args.p

with open(word, "r") as f:
    fh = f.read().split("\n")
    for i in fh:
        ad.put(i)

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1 Safari/603.3.8",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"
]



with open(proxyword, "r") as f:
    fh = f.read().split("\n")
    for i in fh:
        pr.append(i)
# print(pr)
total_items = ad.qsize()

for _ in range(20):
    ad.put(None)


def check(pbar):
    while True:
        word = ad.get()
        if word is None:
            break
        while True:
            try: 
                prx = random.choice(pr)
                user_agent = random.choice(user_agents)
                headers = {"User-Agent": user_agent}
                response = requests.get(f"{url}/{word}", proxies={"http": prx, "https": prx},headers = headers)

                # if response.status_code != 404:
                # print(response.status_code)
                if response.status_code == 200:
                    tqdm.write(f"{Fore.GREEN}[{response.status_code}] {url}/{word} {Style.RESET_ALL} --> {prx}")
                    print(response.status_code)
                elif response.status_code == 303:
                    tqdm.write(f"{Fore.PINK}[{response.status_code}] {url}/{word} {Style.RESET_ALL} --> {prx}")
                elif response.status_code != 404:
                    tqdm.write(f"{Fore.YELLOW}[{response.status_code}] {url}/{word} {Style.RESET_ALL} --> {prx}")
                break  # Break if a valid response is received

            except ProxyError:
                continue
            except RequestException as e:
                continue

        pbar.update(1)
        ad.task_done()

threads = []
pbar = tqdm(total=total_items)

for i in range(20):
    add = threading.Thread(target=check, args=(pbar,))
    add.start()
    threads.append(add)

for thread in threads:
    thread.join()

pbar.close()
print("done")
