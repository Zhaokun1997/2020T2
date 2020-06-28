#!/usr/bin/perl -w

die "Usage: $0 <filename>" if @ARGV != 1;

$filename = shift @ARGV;
$back_version = 0;

open my $in, '<', "$filename" or die "Cannot open $filename: $!\n";
@lines = <$in>;
close $in;

print @lines;

while (-e ".$filename.$back_version")
{
    $back_version++;
}

$back_file = ".$filename.$back_version";
open my $out, '>', $back_file or die "Cannot open $back_file: $!\n";
print $out @lines;
print "Backup of '$filename' saved as '.$filename.$back_version'\n";
close $out;

exit 0;