#!/bin/dash

if test $# -ne 1
then
    echo "Usage: $0 [commit_id]:filename..."
    exit 1
fi

arg1=$1
commit_id=$(echo "$arg1" | cut -d ':' -f1)
filename=$(echo "$arg1" | cut -d ':' -f2)


if echo "$commit_id" | egrep "[0-9]+" > /dev/null  # when commit_id exists
then
    # echo "commit_id is : $commit_id"
    # echo "filename is : $filename"
    if cat .shrug/repo/$commit_id/$filename
    then
        exit 0
    else
        echo "Failed to access .shrug/repo/$commit_id/$filename"
        exit 1
    fi
else  # when commit_id is omitted
    # echo "commit_id is : empty"
    # echo "filename is : $filename"
    if cat .shrug/index/$filename
    then
        exit 0
    else
        echo "Failed to access .shrug/index/$filename"
        exit 1
    fi
fi
