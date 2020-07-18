#!/usr/bin/perl -w


use List::Util qw(max min);

$largest_number = -99999;
@output = ();

while($line = <STDIN>)
{
    while ($line=~ /(-?\d+(\.\d+)?)/g)
    {
        $number = $1;
        if ($number && $number > $largest_number)
        {
            $largest_number = $1;
            @output = ($line);
        }
        elsif ($1 == $largest_number)
        {
            push(@output,$line); 
        }
    }
}
print @output;

exit 0;

# my @result=();
# my $largest=-100000;



# while($line = <STDIN>){
# #select the number
#    while ($line =~ /(-?\d+(\.\d+)?)/g){
#    #one is the every new input 
#       if($largest == -100000 || $1 > $largest){         
#          $largest =  $1;         
#          @result=($line); #if find larger,replace
#       }elsif ($1 == $largest) {
#          push(@result,$line);      
#       }
#    }
# }
# print @result;
