#!/bin/sh

# Description:
# This script updates the compatibility includes to reference the shared
# ones that are copied to docs-shared via GitHub action.
#
# Usage:
# 1) Check out the versioned branch of the docs repo that corresponds to the one 
# that you recently published.
# 2) Run this script from the root of the docs repo.
# 3) Review the changes and follow normal PR review processes.

sed -i '' "s#.. include::[ \t]*/includes#.. sharedinclude:: dbx#g" source/compatibility.txt
