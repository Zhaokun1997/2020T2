#!/bin/dash

if test $# -eq 0 
then
    echo "Usage: $0 filenames..."
    exit 1
fi


for file in "$@"
do
    # if file exists in local, then test filename request 
    # then add to .shrug/index/
    if test -e $file  
    then
        if echo "$file" | egrep "^[a-zA-Z0-9][.-_a-zA-Z0-9]*" > /dev/null
        then
            cp "$file" ".shrug/index/$file"
        else
            echo "bad filename $file!"
            exit 1
        fi
    else
        echo "$file does not exist!"
        exit 1
    fi
done

exit 0