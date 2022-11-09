# Search for code-block indentation issues

import os
import re

# assign directory
directory = 'source'
filename_re = r'\.(txt|rst)$'
code_block_re = r'\.\.\s(io-)*code-block\:\:'
debug = False

# iterate over files in
# that directory
for root, dirs, files in os.walk(directory):
    for filename in files:
        if re.search(filename_re, filename):
            filepath = os.path.join(root, filename)

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                    in_code_block = False
                    curr_spaces = 0

                    if debug:
                        print("Checking file %s" % filepath)

                    for i, line in enumerate(lines):
                        line = line.rstrip()
                        # already in code block
                        if in_code_block:

                            spaces = len(line) - len(line.lstrip())
                            if debug:
                                print("Line: %s spaces: %d" % (line, spaces))
                            if spaces > curr_spaces and spaces < (curr_spaces + 3):
                                print("Bad spacing detected: %s:%d\n%s" % (filepath, i, line))
                                in_code_block = False

                            # exiting a code block
                            if spaces <= curr_spaces and len(line) > 0:
                                if debug:
                                    print("Exiting code block")
                                in_code_block = False

                        # entering code block
                        code_block_search = re.search(code_block_re, line)
                        if code_block_search:
                            if debug:
                                print("Entering code block on line: %d" % i)
                            in_code_block = True
                            curr_spaces = code_block_search.start()
                            if debug:
                                print("Line: %s curr_spaces: %d" % (line, curr_spaces))

                        #if debug:
                        #    if re.search(code_block_re, line):
                        #        print("%s:%d\n%s" % (filepath, i, line))
            except Exception as e:
                print("Unable to process file: %a\n%ss" % (filepath, e))
