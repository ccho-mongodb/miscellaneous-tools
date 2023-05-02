import os
import re
from spellchecker import SpellChecker
import argparse
from collections import Counter

# Usage
# -----
# This script reads files in the relative "source/" directory and sub-directories
# named with the "rst" or "txt" extension and outputs a list of words that occur
# only at a frequency that you specify. By default, the script runs a
# spellchecker on the output list and separates the list
# into words that are spelled correctly and words that are potentially misspelled.
#
# If the same word is capitalized differently in two places, the two
# versions are evaluated separately.
#
# Backstory
# ---------
# A user reported an issue with documentation in which "Atlas" was misspelled
# as "Alas". After investigation, a writer reported there was only one instance
# of the type. Hence, "there was, alas, but one".
#
# Instructions
# ------------
# Make sure you install the required libraries by running `pip install -r requirements.txt`
# Run this file at the same level as your "/source" directory:
# e.g. python3 alas_but_one.py > output.txt
#
# Update the optional `occur_freq` constant in the main method to locate only words that are repeated
# up to n times.
#
# When you run the file, you can include the optional "--noSpellCheck"
# flag to disable the spellchecker function:
# e.g. python3 alas_but_one.py --noSpellCheck > output.txt


def count_in_dir():
    directory = "source"
    filename_re = r"\.(txt|rst)$"
    pattern = re.compile(
        r"(?<!\S)[a-zA-Z0-9]+(?:[-'][a-zA-Z]+)*(?<!'s)[a-zA-Z]?(?=\W|$)"
    )
    # pattern = re.compile(r"\s*(?:[()]|'s|\s|-|`|/|#)\s*")

    fullwordlist = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if re.search(filename_re, filename):
                filepath = os.path.join(root, filename)
                read_file = open(filepath, "r", encoding="utf-8").read()
                f = re.sub("[-,_,.]", " ", read_file)
                words = re.findall(pattern, f)
                fullwordlist += words

    freq = Counter(fullwordlist)

    return freq


def num_occurrences(dict, occur_freq=1):
    occurs_upto_n_times = []
    for key in dict.keys():
        if dict[key] <= occur_freq:
            occurs_upto_n_times.append(key)

    return occurs_upto_n_times


def main():
    parser = argparse.ArgumentParser()
    x = count_in_dir()

    occur_freq = 1
    lst = num_occurrences(x, occur_freq)

    parser.add_argument("--noSpellCheck", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    if args.noSpellCheck:
        header_nocheck = "Words that occur up to {}x:".format(occur_freq)
        print("\n" + header_nocheck)
        print(len(header_nocheck) * "=", *lst, sep="\n- ")
    else:
        spell = SpellChecker(case_sensitive=True)
        spelled = spell.known(lst)
        header_occ1 = "Words that occur up to {}x, but spelled correctly:".format(
            occur_freq
        )
        print("\n" + header_occ1)
        print(len(header_occ1) * "=")

        for w in lst:
            if w.lower() in spelled:
                print("- " + w)

        misspelled = spell.unknown(lst)
        header_misspelled = "Words that occur up to {}x and are misspelled:".format(
            occur_freq
        )
        print("\n" + header_misspelled)
        print(len(header_misspelled) * "=")

        for w in lst:
            if w.lower() in misspelled:
                print("- " + w)


if __name__ == "__main__":
    main()
