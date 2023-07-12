# Deprecated: this tool was designed to make use of the configuration structure 
# of legacy builds. While the script should function, you should use more
# specialized scripts # such as https://github.com/terakilobyte/checker
#
# Send HTTP requests to a collection of URLs
#
# Expects to be run in repository with conf.py containing an extlinks
# associative array and link content in .rst and .txt files.

import os
import re
from collections import defaultdict
import pprint
import json
import urllib.request
import concurrent.futures

from conf import extlinks

HTTP_TIMEOUT = 10
NUM_THREADS = 30
REQUEST_HEADERS = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36' }


link_regex = re.compile(r'<\s*https?://(\S+)\s*>')
extlink_regex = re.compile(r'https?://(\S+)%s')

# extlinks section

valnames = [(re.sub(extlink_regex, r"\1", x[0])) for x in extlinks.values()]

extlinks_expansions = dict(zip(extlinks.keys(), valnames))
extlinks_regex = ":({}):\n*`.*<(.*)>.*`".format("|".join(extlinks.keys()))

# regex: regex to match keys in first group and suffix in second group
# expansions: mapping from the extlinks key name to base url
def fetch_expanded_links(regex, expansions):
    full_urls = []
    for dirpath, dirnames, filenames in os.walk("source"):
        for filename in [f for f in filenames if (f.endswith(".txt") or f.endswith(".rst"))]:
            filepath = "/".join([dirpath, filename])

            with open(filepath, 'r') as file:
                data = file.read()

                for m in re.finditer(extlinks_regex, data):
                    expansion = extlinks_expansions[m.group(1)]
                    if expansion is None:
                        print("WARNING: expansion of extlink was None for {}".format(m.group(1)))
                        continue

                    url_replacement = "{}{}".format(extlinks_expansions[m.group(1)], m.group(2))
                    full_urls.append(url_replacement)

        else:
            continue

    return full_urls

# Only print exceptions to minimize output
def check_url(url):
    try:
        req = urllib.request.Request(url=("https://%s" % url), headers=REQUEST_HEADERS)
        resp = urllib.request.urlopen(req)
    except Exception as e:
        print("* {}: {}".format(url, e))
        pass

def main():
    # compile list of urls
    urls = fetch_expanded_links(extlinks_expansions, extlinks_regex)
    print("{} expanded urls".format(len(urls)))

    for dirpath, dirnames, filenames in os.walk("source"):
        for filename in [f for f in filenames if (f.endswith(".txt") or f.endswith(".rst"))]:
            filepath = "/".join([dirpath, filename])

            with open(filepath, 'r') as file:
                data = file.read()

                for m in re.finditer(link_regex, data):
                    url = m.group(1)

                    if url is not None:
                        urls.append(url)

        else:
            continue

    uniq_urls = set(urls)
    print("{} urls to check".format(len(uniq_urls)))

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            executor.map(check_url, uniq_urls) # , timeout=HTTP_TIMEOUT)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
