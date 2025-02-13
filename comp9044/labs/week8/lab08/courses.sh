#!/bin/sh

# <td class="data"><a href="COMP9313.html">COMP9313</a></td>
# <td class="data"><a href="COMP9322.html">Software Service Design and Engineering</a></td>

if test $# != 1
then
    echo "Usage: $0 <course-prefix>"
    exit 1
fi

# arg1="$1"
# curl --location --silent http://www.timetable.unsw.edu.au/current/$1KENS.html | 
# egrep "<a href=\"$1[0-9]+\.html\">.*</a></td>" | 
# egrep -v "<a href=\"$1[0-9]+\.html\">$1[0-9]+</a></td>" |
# egrep -o "$1.*<" | 
# sort | 
# uniq -w 8|
# sort -n |
# while read line  
# do
#     # echo "$line"
#     code=$(echo "$line" | egrep -o "$1[0-9]+")
#     # pattern="\<\/a\>\<"
#     name=$(echo "$line" | egrep -o "html\">.+<" | sed s/html\"\>//g | cut -d '<' -f1)
#     echo "$code" "$name"
# done


course=$1
url="http://www.timetable.unsw.edu.au/current/"$course"KENS.html" 

wget -q -O- "$url"|
egrep "$course[0-9]{4}.html"|
sed "s/.*\($course[0-9][0-9][0-9][0-9]\)\.html[^>]*> *\([^<]*\).*/\1 \2/"|
egrep -v $course[0-9]{4}.$course[0-9]{4}|
sed 's/ *$//'|
sort|
uniq