#!/usr/bin/perl -w
# use strict;

# foreach $arg (@ARGV) {
#     print $arg, " ";
# }
# print "\n";

# print "@ARGV\n";
# print join(",", @ARGV), "\n"

$sum = 0;
foreach $arg (@ARGV)
{
    $sum += $arg;
}

print "Sum of the numbers is $sum\n";