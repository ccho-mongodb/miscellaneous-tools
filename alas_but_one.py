import os
import re
from spellchecker import SpellChecker
import argparse
from collections import Counter

# Usage
# -----
# This script reads files in the relative "source/" directory and sub-directories
# named with the "rst" or "txt" extension and outputs a list of words
# and the frequency at which each word occurs in the directory files. The
# maximum word frequency for the output list is 1 by default, but you
# can optionally specify this value. By default, the script runs a
# spellchecker on the output list and separates the list
# into words that are spelled correctly and words that are potentially
# misspelled.
#
# You should check both lists to find words that are
# potentially out of place in the documentation, as the main purpose of the
# frequency analysis is to find incorrectly placed words that *are* spelled correctly.
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
# When you run the file, you can optionally specify the maximum word
# frequency and enable/disable the spellchecker.
# For example, to set the frequency to 2 and disable the spellchecker, run:
# python3 alas_but_one.py --freq 2 --no-spellCheck
#
# If you enable the spellchecker (as it is by default), you can also
# specify the "--hideMisspelled" flag to see the list of words that
# are spelled correctly:
# e.g. python3 alas_but_one.py --hideMisspelled


def count_in_dir():
    directory = "source"
    filename_re = r"\.(txt|rst)$"

    # this regular expression includes the following components:
    # - negative lookbehind to check that there is no non-whitespace
    #   character before the word
    # - expression matching any alphanumeric string that may contain
    #   hyphens or apostrophes
    # - negative lookbehind assertion to exclude words ending with "'s"
    #   (e.g., possessives) from matching.
    # - positive lookahead to ensure that the match is followed by a
    #   non-alphanumeric character or end of the string

    pattern = re.compile(r"(?<!\S)[a-zA-Z0-9]+(?:[-'][a-zA-Z]+)*(?<!'s)(?=\W|$)")

    wordlist = []

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if re.search(filename_re, filename):
                filepath = os.path.join(root, filename)
                read_file = open(filepath, "r", encoding="utf-8").read()
                f = re.sub("[-,_,.]", " ", read_file)
                words = re.findall(pattern, f)
                wordlist += words

    freq = Counter(wordlist)

    return freq


def num_occurrences(ctr, occur_freq=1):
    occurs_upto_n_times = {k: v for k, v in ctr.items() if v <= occur_freq}

    return occurs_upto_n_times


def main():
    parser = argparse.ArgumentParser(
        description="Find words in this repo that appear up to N times and optionally run a spellchecker."
    )
    parser.add_argument(
        "--freq",
        metavar="N",
        type=int,
        help="words appear at this frequency or less (default: 1)",
        default=1,
    )
    parser.add_argument(
        "--spellCheck",
        action=argparse.BooleanOptionalAction,
        help="enable or disable the spellchecker feature",
        default=True,
    )
    parser.add_argument(
        "--hideMisspelled",
        action=argparse.BooleanOptionalAction,
        help="don't see list of misspelled words",
    )

    args = parser.parse_args()

    x = count_in_dir()
    lst = num_occurrences(x, args.freq)
    sorted_lst = dict(sorted(lst.items(), key=lambda x: x[1], reverse=True))

    if args.spellCheck:
        spell = SpellChecker(case_sensitive=True)
        spelled = spell.known(sorted_lst)
        header_occ1 = "Words that occur up to {}x, but are spelled correctly:".format(
            args.freq
        )
        print("\n" + header_occ1)
        print(len(header_occ1) * "=")

        for w in sorted_lst:
            if w.lower() in spelled:
                print(f"- {w} ({lst[w]})")

        if not args.hideMisspelled:
            misspelled = spell.unknown(sorted_lst)
            header_misspelled = "Words that occur up to {}x and are misspelled:".format(
                args.freq
            )
            print("\n" + header_misspelled)
            print(len(header_misspelled) * "=")

            for w in sorted_lst:
                if w.lower() in misspelled:
                    print(f"- {w} ({lst[w]})")
    else:
        header_nocheck = "Words that occur up to {}x:".format(args.freq)
        print("\n" + header_nocheck)
        print(len(header_nocheck) * "=")

        for w in sorted_lst:
            print(f"- {w} ({lst[w]})")


if __name__ == "__main__":
    main()
