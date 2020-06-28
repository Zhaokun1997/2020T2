#!/usr/bin/perl -w

$line_count = 0;
# while (1)
# {
#     $line = <STDIN>;
#     last if !$line;
#     # if (!$line)
#     # {
#     #     last;
#     # }
#     $line_count++;
# }

# while (<STDIN>)
# {
#     $line_count++;
# }

while ($line = <>)
{
    print "$line";
}

print "$line_count lines\n";
exit 0;