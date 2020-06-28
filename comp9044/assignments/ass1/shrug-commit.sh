#!/bin/dash

if test $# -ne 2 || test "$1" != "-m"
then
    echo "Usage: $0 -m <message>..."
    exit 1
fi

# ./shrug-commit.sh -m "first commit"

# content shrug.log:
# 1 second commit
# 0 first commit


commit_files()
{
    # step 1: make current commit directory
    # attention:
    # we do not need to clear index/ every time
    if mkdir ".shrug/repo/$1"
    then
        # step 2: copy files from index to repo/n/
        for temp_file in .shrug/index/*
        do
            cp "$temp_file" ".shrug/repo/$1/"
        done

        # step 3: echo >> a commit to log
        echo "$1 $message" > .shrug/shrug.log.tm  # temp file
        if cat .shrug/shrug.log >> .shrug/shrug.log.tm
        then
            if mv .shrug/shrug.log.tm .shrug/shrug.log
            then
                echo "Committed as commit $1"
                exit 0
            fi
        fi
    else
        echo "Failed to make dir: .shrug/repo/$1"
        exit 1
    fi
}


message=$2

# about commit_id
if cat .shrug/shrug.log | egrep "." > /dev/null  # if shrug.log has content
then
    commit_id=$(cat .shrug/shrug.log | cut -d ' ' -f1 | head -1)
    commit_id=$((commit_id + 1))
    commit_files "$commit_id"

else  # when shrug.log has no commit records
    commit_id=0
    commit_files "$commit_id"
fi
exit 0