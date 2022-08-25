import sys, csv, re, collections

# This script removes version from docs URLs and aggregates the unique page view totals
#
# Usage: python dedupe_analytics.py <Google Analytics report csv file>
#
# Workflow for adding deduped analytics to Google Analytics report sheet:
# 1) Export the Google Analytics report sheet to a CSV file
# 2) Remove any rows in the CSV file that occur before the headers for the analytics
# 3) Run this script, piping the output to a new CSV file
# 4) In the Google sheet, import the CSV file you generated
# 5) Select "Insert into new spreadsheet(s)" in order to populate the data from the CSV in a new tab


# Uncomment the "URL_VERSION_RE" regular expression constant appropriate for the property
# drivers
URL_VERSION_RE = r"^www\.mongodb\.com\/docs\/drivers\/([\-\/\w+]*)\/(current?|v[0-9]+\.[0-9]+?)\/([#\?\-\/\w+]*)(\?.*)?$"

# connectors
#URL_VERSION_RE = r"^www\.mongodb\.com\/docs\/([\-\/\w+]*)/(current?|[0-9]+\.[0-9]+?)\/([#\?\-\/\w+]*)(\?.*)?$"

# GH pages
#URL_VERSION_RE = r"^mongodb\.github\.io\/([\-\/\w+]*)/(current?|[0-9]+\.[0-9]+?)\/([#\?\-\/\w+]*)(\?.*)?$"

with open(sys.argv[1]) as csvfile:
    results = {}

    fh = csv.DictReader(csvfile, delimiter=',')
    for row in fh:
        if (matches := re.match(URL_VERSION_RE, row['Page'])) is not None:

            url = "%s/%s" % (matches.group(1), matches.group(3))
            total = int(row['Unique Pageviews'])

            # zero the value if entry doesn't exist
            results[url] = results.get(url, 0) + total

    # sort by second column (unique page views)
    sorted_results = collections.OrderedDict(sorted(results.items(), key=lambda item: -item[1]))

    for k,v in sorted_results.items():
        print("%s,%s" % (k,v))
