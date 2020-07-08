#!/usr/bin/perl -w

# die "Usage: $0 <word> < <file_as_STDIN>\n" if @ARGV != 1;

# $query_word = shift @ARGV;


foreach $file (glob "lyrics/*.txt") 
{
    # get artist name
    $artist_name = $file
    $artist_name =~ s/^lyrics\///;
    $artist_name =~ s/\.txt//;
    $artist_name =~ tr/_/ /;

    open my $in, '<', "$file" or die "Cannot open $file: $!\n";
    
    while ($line = <$in>)
    {
        @words = $line =~ /[a-zA-Z]+/g;
        foreach $word (@words)
        {
            $word =~ tr/[A-Z]/[a-z]/;
            $words_hash{"$word"}++;
        }
    }
    close $in;
}



# if (!$words_hash{$query_word})
# {
#     print "$query_word occurred 0 times\n";
# }
# else
# {
#     print "$query_word occurred $words_hash{$query_word} times\n";
# }
