# dirfinder

A Python script for multithreaded checking of URLs using proxies. The script reads a base URL and a wordlist, then constructs full URLs by appending each word from the wordlist to the base URL. It sends HTTP GET requests to these URLs concurrently using multiple threads with random user agents and proxies.

## Features

- Uses threading to perform concurrent URL checking for faster execution.
- Randomizes User-Agent headers to simulate different browsers.
- Supports proxy usage from a proxy list to anonymize requests.
- Handles HTTP status codes and highlights results with colored output.
- Uses progress bar (`tqdm`) to indicate progress.

## Requirements

- Python 3.x
- `requests`
- `tqdm`
- `colorama`

- 
## Usage

`python url_checker.py -u <base_url> [-w <wordlist_file>] [-p <proxy_list_file>]`
text

- `-u`: Base URL to check (required). Example: `http://example.com`
- `-w`: Path to the wordlist file (default: `wordlist.txt`). Each line is appended to the base URL.
- `-p`: Path to the proxy list file (default: `wordlist.txt`). Each line should contain a proxy address.



## Example:

`python url_checker.py -u http://example.com -w paths.txt -p proxies.txt`

This will read paths from paths.txt and proxies from proxies.txt, then check URLs like http://example.com/<path> using the proxies.

## How it works:

The script loads the wordlist and proxy list into memory.
It uses 20 worker threads to process the URLs in parallel.
Each thread picks a word from the queue, selects a random proxy and user agent, and sends a GET request.
Response codes are printed with colored output for easy recognition.
Progress bar shows checking progress.


