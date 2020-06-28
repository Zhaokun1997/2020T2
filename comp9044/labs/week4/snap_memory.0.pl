#!/usr/bin/perl -w

while (1)
{
    print "Enter line: ";
    $line = <STDIN>;
    last if (!defined $line);
    print "Snap!\n" if $seen{$line};
    $seen{$line} = 1;
}