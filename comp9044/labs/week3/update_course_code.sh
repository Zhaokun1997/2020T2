#!/bin/sh
# doesn't hande pathnames containing new lines
# echo "$@"
# find "$@" -type f|
# while read file
# do
#     echo "$file"
# done

find "$@" -type f | cat -et