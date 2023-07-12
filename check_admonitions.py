# Deprecated: the latest Snooty parser currently render admonitions that lack
# a line break correctly now. This could still be useful for legacy builds.
#
# Search for admonitions that lack a line break

import os
import re

# assign directory
directory = 'source'
filename_re = r'\.(txt|rst)$'
admonition_re = r'\.\.\s(warning|tip|danger|note|important|caution|see)\:\:\n +\w+'

# iterate over files in
# that directory
for root, dirs, files in os.walk(directory):
    for filename in files:
        if re.search(filename_re, filename):
            filepath = os.path.join(root, filename)

            with open(filepath, 'r') as file:
                try:
                    content = file.read()

                    # find admonitions
                    search_result = re.findall(admonition_re, content)
                    if search_result:
                        print("%s %s" % (filepath, search_result))
                except:
                    print("Failed to process file: %s" % filepath)
