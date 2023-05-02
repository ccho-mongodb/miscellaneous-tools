import os
import re
from collections import Counter

# Usage
# -----
# This script reads files in the relative "source/" directory and sub-directories
# named with the "rst" or "txt" extension and counts the instances of each
# word (as matched by the WORD_REGEX constant).
# Update the MAX_OCCUR=n constant to print out only words that are repeated
# up to n times.
#
# Backstory
# ---------
# A user reported an issue with documentation in which "Atlas" was misspelled 
# as "Alas". After investigation, a writer reported there was only one instance 
# of the type. Hence, "there was, alas, but one".

MAX_OCCUR=1
OUTPUT_FILE='alas_output.txt'
EXCLUSION_FILE="alas_exclude.txt"
WORD_REGEX=re.compile("[\w'_\-]+")

directory = 'source'
filename_re = r'\.(txt|rst)$'

word_list = []
for root, dirs, files in os.walk(directory):
    for filename in files:
        if re.search(filename_re, filename):
            filepath = os.path.join(root, filename)
            try:
                word_list += re.findall(WORD_REGEX, open(os.path.join(root, filename), 'r', encoding='utf-8').read().lower())
            except Exception as e:
                print(e)

ctr = Counter(word_list)
if os.path.isfile(EXCLUSION_FILE):
    exclusion_list = open(EXCLUSION_FILE).read()
    for w,v in sorted(ctr.items(), key=lambda pair: pair[1], reverse=True):
        if (v <= MAX_OCCUR):
            if (not(w in exclusion_list)):
                print("%s [%d]" % (w,v), file=open(OUTPUT_FILE, 'a'))
else:
    for w,v in sorted(ctr.items(), key=lambda pair: pair[1], reverse=True):
        if (v <= MAX_OCCUR):
            print("%s [%d]" % (w,v), file=open(OUTPUT_FILE, 'a'))
