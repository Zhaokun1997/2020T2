#!/usr/bin/perl -w

die "Usage: $0 <line_index> <file>" if @ARGV != 2;

$line_index = shift @ARGV;
$file = shift @ARGV;

open my $in, '<', $file or die "Cannot open $file: $!";
@lines = <$in>;
print "the $line_index-th line is : $lines[$line_index]\n";
close $in;
exit 0;

