import os
import re
from collections import Counter

# Usage
# -----
# The main purpose of this script is to identify atomic typos by using
# word frequency to identify the candidates.
# It is currently hard-coded to read files in the relative "source/" directory
# and sub-directories named with the "rst" or "txt" extension and counts the instances
# of each word (as matched by the WORD_REGEX constant).
# Update the MAX_OCCUR=n constant to print out only words that occur
# up to n times.
#
# Backstory
# ---------
# A user reported an issue with documentation in which "Atlas" was misspelled 
# as "Alas". After investigation, a writer reported there was only one instance 
# of the type. Hence, "there was, alas, but one".

MAX_OCCUR=1
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
for w,v in sorted(ctr.items(), key=lambda pair: pair[1], reverse=True):
    if (v <= MAX_OCCUR):
        print("%s [%d]" % (w,v))

