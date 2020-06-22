#!/usr/bin/perl -w

# $a[0] = "first string";
# $a[1] = "2nd string";
# $a[2] = 123;
# or, equivalently,
# @a = ("first string", "2nd string", 123);
# print "Index of last element is $#a\n";
# print "Number of elements is ", $#a+1, "\n";

$marks = "99, 67, 85";
@list_marks = split(/, /, $marks);
# $sum = 0;
print "$#list_marks\n";
print "$list_marks[$#list_marks]\n";
print "@list_marks\n";


@nums = (1, 2, 3, 4, 5);
$sum = 0;
# @nums in scalar context gives length 
for ($i = 0; $i < @nums; $i++) 
{
    $sum += $nums[$i];
    print "sum currently is : $sum\n";
}
print "$#nums\n";
print "$nums[$#nums]\n";
print "@nums\n";
# foreach $num (@nums) { sum += $num; }