#!/bin/sh
# written by andrewt@cse.unsw.edu.au as a COMP2041 example
# Print the integers 1..n if 1 argument given.
# Print the integers  n..m if 2 arguments given.

if test $# = 1
then
    start=1
    finish=$1
elif test $# = 2
then
    start=$1
    finish=$2
else
    echo "Usage: $0 <start> <finish>" 1>&2
    exit 1
fi

for argument in "$@"
do
    # clumsy way to check if argument is a valid integer
    if echo "$argument"|egrep -v '^-?[0-9]+$' >/dev/null
    then
        echo "$0: argument '$argument' is not an integer" 1>&2
        exit 1
    fi
done

number=$start
while test $number -le $finish
do
    echo $number
    number=`expr $number + 1`    # or number=$(($number + 1))
done
