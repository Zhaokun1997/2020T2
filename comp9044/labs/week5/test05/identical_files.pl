#!/usr/bin/perl -w


die "Usage: $0 <infile> <outfile>\n" if @ARGV != 2;



while ($line = <$in>)
{
    @all_words = split(/\s+/, $line);
}



# iterate files
foreach ($i = 0; i < @ARGV; i++)
{
    if ($i == 0)
    {
        open my $in, '<', "$ARGV[$i]" or die "Cannot open $ARGV[$i]: $!\n";
        @contents = <$in>;
    }
    open my $in, '<', "$ARGV[$i]" or die "Cannot open $ARGV[$i]: $!\n";
    if (@contents)
    {
        @temp_file = <$in>;
        $file1 = join ("", @contents);
        $file2 = join ("", @temp_file);
        if ($file1 ne $file2)
        {
            print "files are not identical";
        }

    }
}

