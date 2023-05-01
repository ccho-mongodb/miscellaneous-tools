import os
import re
from spellchecker import SpellChecker
from collections import defaultdict
import string
import argparse

# Usage
# -----
# This script reads files in the relative "source/" directory and sub-directories
# named with the "rst" or "txt" extension and outputs a list of words that occur
# only at a frequency that you specify. By default, the script runs a
# spellchecker on the output list and separates the list
# into words that are spelled correctly and words that are potentially misspelled.
#
# Backstory
# ---------
# A user reported an issue with documentation in which "Atlas" was misspelled
# as "Alas". After investigation, a writer reported there was only one instance
# of the type. Hence, "there was, alas, but one".
#
# Instructions
# ------------
# Run this file at the same level as your "/source" directory.
# Update the OCCUR_FREQ=n constant in the main method to locate only words that are repeated
# up to n times.
# When you run the file, you can include the optional "--noSpellCheck"
# flag to disable the spellchecker function:
# e.g. python3 alas_but_one.py --noSpellCheck > output.txt


def count_in_dir():
    directory = "source"
    filename_re = r"\.(txt|rst)$"
    pattern = re.compile(r"\s*(?:[()]|'s|\s|-|`|/|#)\s*")

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
                    words = pattern.split(line)

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
    occurs_upto_n_times = []
    for key in dict.keys():
        if dict[key] <= n:
            occurs_upto_n_times.append(key)

    return occurs_upto_n_times


def main():
    parser = argparse.ArgumentParser()
    x = count_in_dir()

    OCCUR_FREQ = 1
    lst = num_occurrences(x, OCCUR_FREQ)

    parser.add_argument("--noSpellCheck", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    if args.noSpellCheck:
        header_nocheck = "Words that occur up to {}x:".format(OCCUR_FREQ)
        print("\n" + header_nocheck)
        print(len(header_nocheck) * "=", *lst, sep="\n- ")
    else:
        spell = SpellChecker()
        spelled = spell.known(lst)
        header_occ1 = "Words that occur up to {}x, but spelled correctly:".format(
            OCCUR_FREQ
        )
        print("\n" + header_occ1)
        print(len(header_occ1) * "=", *spelled, sep="\n- ")

        misspelled = spell.unknown(lst)
        header_misspelled = "Words that occur up to {}x and are misspelled:".format(
            OCCUR_FREQ
        )
        print("\n" + header_misspelled)
        print(len(header_misspelled) * "=", *misspelled, sep="\n- ")


if __name__ == "__main__":
    main()
