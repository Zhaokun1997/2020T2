#!/usr/bin/perl -w

die "Usage: $0 <infile> <outfile>\n" if @ARGV != 2;

$infile = shift @ARGV;
$outfile = shift @ARGV;

# method_1:
open my $in, '<', $infile or die "Cannot open $infile: $!";
open my $out, '>', $outfile or die "Cannot open $outfile:$!";

# loop could also be written in one line:
# print OUT while <IN>;

# the default variable $_
while (<$in>)
{
    print $out;
}


# method_1:
# open my $in, '<', $infile or die "Cannot open $infile: $!";
# @lines = <$in>
# close $in

# open my $out, '>', $outfile or die "Cannot open $outfile: $!";
# print $out @lines;
# close $out;





exit 0;