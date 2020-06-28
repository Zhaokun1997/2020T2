#!/bin/sh

if test $# != 2
then
    echo "Usage: $0 <start> <end>" 1>&2
    exit 1
fi


start=$1
end=$2

number=$start
while test $number -le $end
do
    echo "$number "
    number=$((number + 1))
done
