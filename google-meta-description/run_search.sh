#!/usr/bin/sh

# Usage:
# $ google_results urls.txt

# Avoid illegal character in MacOS
export LANG=C

# Function from https://github.com/sfinktah/bash/blob/master/rawurlencode.inc.sh
rawurlencode() {
    local string="${1}"
    local strlen=${#string}
    local encoded=""
    local pos c o

    for (( pos=0 ; pos<strlen ; pos++ )); do
        c=${string:$pos:1}
        case "$c" in
           [-_.~a-zA-Z0-9] ) o="${c}" ;;
           * )               printf -v o '%%%02x' "'$c"
        esac
        encoded+="${o}"
    done
    echo "${encoded}"    # You can either set a return variable (FASTER) 
    REPLY="${encoded}"   #+or echo the result (EASIER)... or both... :p
}

echo "URL,Search_String,Meta_Description"

for url in $(cat $1);
do
  NEW_URL=$(echo $url | sed -e 's/\r//g')
  SEARCH_STR="https://www.google.com/search?q=$( rawurlencode $NEW_URL)"

  # Pull content using lynx
  # Print content starting at "[5]" and ending at "[6]"
  lynx -dump $SEARCH_STR
  #META_DESC=$(lynx -dump $SEARCH_STR | sed -n -e '/\[5\]/,/\[6\]/{ /\[6\]/d; p; }')
  
  #echo "${NEW_URL},${SEARCH_STR},\x22${META_DESC}\x22"
  sleep 3
done
