import os
import re
from spellchecker import SpellChecker

from collections import defaultdict
import string

# Usage
# -----
# This script reads files in the relative "source/" directory and sub-directories
# named with the "rst" or "txt" extension and counts the instances of each
# word.
# Update the occur_freq=n constant to print out only words that are repeated
# up to n times.
#
# Backstory
# ---------
# A user reported an issue with documentation in which "Atlas" was misspelled
# as "Alas". After investigation, a writer reported there was only one instance
# of the type. Hence, "there was, alas, but one".


def count_in_dir():
    directory = "source"
    filename_re = r"\.(txt|rst)$"

    processed = []
    words_and_freqs = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if re.search(filename_re, filename):
                filepath = os.path.join(root, filename)
                # print(filepath)
                read_file = open(filepath, "r", encoding="utf-8")
                # processed = []

                for line in read_file:
                    line = line.strip()
                    words = re.split(r"\s*(?:[()]|'s|\s|-|`|/|#)\s*", line)

                    for word in words:
                        pword = word.strip(string.punctuation)
                        processed.append(pword.lower())

    for elem in processed:
        if elem != None:
            words_and_freqs.append(elem)

    freq = defaultdict(int)
    for item in words_and_freqs:
        freq[item] += 1

    return freq


def num_occurrences(dict, n):
    occurs_n_times = []
    for key in dict.keys():
        if dict[key] == n:
            occurs_n_times.append(key)

    return occurs_n_times


def main():
    spell = SpellChecker()
    x = count_in_dir()

    occur_freq = 1
    lst = num_occurrences(x, occur_freq)
    spelled = spell.known(lst)

    header_occ1 = "Words that occur only {}x, but spelled correctly:".format(occur_freq)
    print("\n" + header_occ1)
    print(len(header_occ1) * "=", *spelled, sep="\n- ")

    misspelled = spell.unknown(lst)
    header_misspelled = "Words that occur only {}x and misspelled:".format(occur_freq)
    print("\n" + header_misspelled)
    print(len(header_misspelled) * "=", *misspelled, sep="\n- ")


if __name__ == "__main__":
    main()
