import csv
import re
import collections

# This script removes version from docs URLs and aggregates the unique page view totals

# server
URL_VERSION_RE = "(www\.mongodb\.com\/docs)\/(upcoming|current|v[0-9]+\.[0-9]+?)\/([#\?\-\/\w+]*)"

# drivers
#URL_VERSION_RE = r"^docs\.mongodb\.com\/drivers\/([\-\/\w+]*)/(current?|[0-9]+\.[0-9]+?)\/([#\?\-\/\w+]*)"

# connectors
#URL_VERSION_RE = r"^docs\.mongodb\.com\/([\-\/\w+]*)/(current?|[0-9]+\.[0-9]+?)\/([#\?\-\/\w+]*)"

# GH pages
#URL_VERSION_RE = r"^mongodb\.github\.io\/([\-\/\w+]*)/(current?|[0-9]+\.[0-9]+?)\/([#\?\-\/\w+]*)"

with open('report.csv') as csvfile:

    results = {}

    fh = csv.DictReader(csvfile, delimiter=',')
    for row in fh:
        matches = re.match(URL_VERSION_RE, row['Page']);

        if matches:
            url = "%s/%s" % (matches.group(1), matches.group(3))
            total = int(row['Unique_Pageviews'])
            results[url] = results.get(url, 0) + total


    sorted_results = collections.OrderedDict(sorted(results.items(), key=lambda item: -item[1]))
    for k,v in sorted_results.items():
        print("%s,%s" % (k,v))
