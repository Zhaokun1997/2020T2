die "Usage: $0 <n>\n" if @ARGV != 1;
# print "ARGV[0] is : $ARGV[0] \n";
$n = 0;
$string = '@';
while ($n < $ARGV[0])
{
    $string = "$string$string";
    $n++;
}

printf "String of 2^%d = %d characters created\n", $n, length $string;