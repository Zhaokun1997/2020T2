#!/bin/sh


RANDOM=$$
s=$RANDOM
RANDOM=$$
size=$(($RANDOM % 300))
e=$(($size + $s))



while test $s -le $e
do
   lines="$s"$'\n'"$lines";
   s=$(expr $s + 1);
done
t=$(echo "$lines" | sed "/^$/d"|./shuffle.pl|sort)
r=$(echo "$lines" | sed "/^$/d"|sort)

if test "$t" = "$r" 
then
   echo "pass"
else

   echo "fail"
fi

