import re, sys
import csv

expr = re.compile(r'\[5\](.*?)\[6\]', re.DOTALL)

link_file = open(sys.argv[1], encoding="utf8", errors="ignore")
links = link_file.readlines()
link_file.close()

content_file = open(sys.argv[2], encoding="utf8", errors="ignore")
content = content_file.read()
content_file.close()

with open(sys.argv[3], 'w', encoding="utf8", errors="ignore") as csvfile:
    try:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')

        search_result = re.findall(expr, content)
        print("Matches: %d" % len(search_result))
        for i, val in enumerate(search_result):
            link_text = ''.join(links[i].splitlines())
            desc_text = ''.join(val.splitlines())

            csvwriter.writerow([link_text, desc_text])

    except Exception as e:
        print(e)
