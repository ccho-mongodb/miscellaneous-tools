# Google Meta Descriptions Scraper

This collection of scripts makes the task of extracting the description,
which corresponds to the [meta description](https://moz.com/learn/seo/meta-description),
from a Google search result.

# Scripts and Tasks

The following sections describe how to accomplish specific tasks that might
be related to your workflow for extracting the meta description data.

## Download Sitemaps

Download the sitemap xml file to get a list of URLs that belong to that site.
Redirect the output to a file. If you already have a list of URLs, proceed
to the **Open the URLs and Scrape the Data** step.

For example, the following ``curl`` command downloads the XML sitemap file
for the MongoDB Golang Driver:

```bash
curl "https://www.mongodb.com/docs/drivers/go/current/sitemap.xml" > go_sitemap_urls.xml
```

## Extract URLs From a Sitemap File

Use the ``xq`` tool to extract the URLs from the sitemap file.

To install ``xq`` on MacOS, use the following Homebrew command:

```bash
brew install xq
```

To extract the URLs b y using ``xq``, specify the Xpath and redirect the
output to a file. For example:

```bash
xq -x '/urlset/url/loc' go_sitemap_urls.txt > go_urls.txt
```

## Open the URLs and Scrape the Data

Install the ``lynx`` text browser. In MacOS, use the following Homebrew
command:

```bash
brew install lynx
```

Use the ``run_search.sh`` script to start scraping the URLs specified in your
file, and redirect the output to another file:

```bash
sh run_search.sh go_urls.txt > go_results.txt
```

**Important**: Google blocks your requests if you send >100 per hour from
a single IP address. To avoid this limit, distribute your requests across
machines with different IPs and send fewer than 100 in an hour.

If Google blocks your requests, the script will not fail, but the result
file will contain the following text instead of the search result and might
cause further data processing to fail:

> In order to continue, please enable javascript on your web browser.


## Generate a CSV file from the Results

Use the ``extract_and_zip_results.py`` Python script to extract the text that
corresponds to the meta description and the input file used in the previous
step to output a CSV file. For example, the following command calls the
script and writes the results to the ``go_meta_descriptions.csv`` file:

```
python3 extract_and_zip_results.py go_urls.txt go_results.txt go_meta_descriptions.csv
```
