import os
import re
import argparse;
from collections import Counter

# Usage
# -----
# This script reads files in the relative "source/" directory and sub-directories
# named with the "rst" or "txt" extension and counts the instances of each
# word (as matched by the WORD_REGEX constant).
# Update the MAX_OCCUR=n constant to print out only words that are repeated
# up to n times.
#
# Optional Modifiers
# ------------------
# --noCount
#   Produces output of words matching the conditions without a count of how
#   often the words occur. 
#
# --output <file>
#   Writes the output of the script to the specified output file. This will
#   delete any current contents of the file before writing the output.
#
# --exclusion <file>
#   Takes the specified file and creates a list of words to exclude. Any words
#   that are on the exclusion list will not be included in the output. The
#   expected format of the exclusion file is each excluded word is on its own
#   line. Tip: the easiest way to create an exclusion list is to create an
#   output file with the --noCount option and use that file after verifying
#   all words on that list are acceptable instances.
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

parser = argparse.ArgumentParser()
parser.add_argument('--exclusion', type=str)
parser.add_argument('--output', type=str)
parser.add_argument('--noCount', action=argparse.BooleanOptionalAction)
args=parser.parse_args()

if args.exclusion:
    if (os.path.isfile(args.exclusion)):
        doExclusion = True
        with open(args.exclusion, 'r') as f:
            exclusion_list = f.read().splitlines()
    else:
        doExclusion = False
        print("Error: Exclusion not performed. Exclusion file %s not found" % (args.exclusion))
if args.output:
    if (os.path.isfile(args.output)):
        with open(args.output, 'r+') as file:
            file.truncate(0)

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
    addWord=((v <= MAX_OCCUR) and
             (not(doExclusion) or
                (doExclusion and not(w in exclusion_list))))
    if addWord:
        if args.noCount:
            outputString="%s" % (w)
        else:
            outputString="%s [%d]" % (w,v)
        if args.output:
            print(outputString, file=open(args.output, 'a'))
        else:
            print(outputString)