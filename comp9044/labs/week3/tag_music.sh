#!/bin/sh

# test argument form
# if test $# != 0
# then
#     echo "Usage $0: <nothing>" 1>&2
#     exit 1
# fi

id3_Title=""
id3_Album=""
id3_Year=""
id3_Track=""
id3_Artist=""

# dir_name=$(echo "$@" | cut -d/ -f1)
# dir_name=$(dirname "$1")
# echo $dir_name
for directory in "$@"
do
    find "$directory" -type f -name *.mp3 | 
    while read line
    do
        echo "$line"    # tiny_music/Album1, 2015/1 - Riptide - Vance Joy.mp3
        info=$(echo "$line" | cut -d '/' -f2-)  # Album1, 2015/1 - Riptide - Vance Joy.mp3
        echo "$info"
        id3_Album=$(echo "$info" | cut -d '/' -f1)  # Album1, 2015
        id3_Year=$(echo "$id3_Album" | cut -d ',' -f2 | sed 's/^ *//')  # 2015
        id3_Track=$(echo "$info" | cut -d '/' -f2 | cut -d '-' -f1 | sed 's/ *$//')  # 1
        id3_Title=$(echo "$info" | cut -d '/' -f2 | cut -d '-' -f2 | sed 's/^ *//' | sed 's/ *$//')  # Riptide
        id3_Artist=$(echo "$info" | cut -d '/' -f2 | sed 's/- []/'
        #cut -d '-' -f3 | sed 's/^ *//' | sed 's/.mp3$//')  # Vance Joy
        # id3tag --album="$id3_Album" --year="$id3_Year" --track="$id3_Track" --comment="$id3_Title" --artist="$id3_Artist" "$line"
        echo "id3_Artist is : $id3_Artist"
    done
done
