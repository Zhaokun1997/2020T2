#!/usr/bin/perl -w

$sum = 0;
while ($line = <STDIN>) {
    $line =~ s/^\s*//; # remove leading white space
    $line =~ s/\s*$//; # remove leading trailing white space
    # Test if string looks like an integer or real (scientific notation not handled!)
    if ($line !~ /^\d[.\d]*$/) {
        last;
    }
    $sum += $line;
}
print "Sum of the numbers is $sum\n";