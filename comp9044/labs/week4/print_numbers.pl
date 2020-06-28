#!/usr/bin/perl -w

die "Usage: $0 <start> <end>\n" if @ARGV != 2;


$start = shift @ARGV;
$end = shift @ARGV;

for ($number = $start; $number <= $end; $number++)
{
    print "$number ";
}
print "\n";
exit 0;

