## TEST 用法

    test -e "$file_name"  && continue
    
    test -e "$file_name"  && break
    
    test "$msg" = "Hello"
    
    test "$x" -gt "$y"
    
    test "$x" -lt "$y" -a "$x" -gt "%z"
    
    test -r xyz
    
    test -z xyz
   
    test -d abc
    
## For 循环语句

    sum=0
    for n in "$@" # use "$@" to preserve args
    do
        sum=‘expr $sum + "$n"‘
    done
    
    
    
    for file in *
    do
        echo "$file"
    done
    
    
    for file in $(ls *.h)
    do
        echo "$file"
    done
    
##  IF的写法解释  
    if grep "^$user" /etc/passwd > /dev/null
    then
        # do something if they do exist ...
    else
        echo "$0: $user does not exist"
    fi 
## 小知识点总结

    https://cgi.cse.unsw.edu.au/~cs2041/20T2/code/shell/index
    
    touch a.txt
    
    echo 'hello world' > a.txt
    
    
    egrep -v '^$'|            # remove empty lines
    
    
    # This use of a regex is a bash extension missing from many Shells
    # It should be avoided if portability is a concern
    if ! [[ "$argument" =~ ^-?[0-9]+$ ]]
    then
        echo "$0: argument '$argument' is not an integer" 1>&2
        exit 1
    fi
    
    
    # remove -
    mv -- "$filename" "$new_filename"
    
    
    sed 's/\/\/.*//' "$file1" >$TMP_FILE1
    substitutions='s/\/\/.*//;s/"[^"]"/s/g;s/[a-zA-Z_][a-zA-Z0-9_]*/v/g'
    
## Perl 语言
    
    perl5/perl6
    
    use warnings;
    use strict;
    

## Perl的数据类型

    $x = abc; is the same as $x = "abc";
    
    Char Kind Example Description
    # Comment # comment rest of line is a comment
    $ Scalar $count variable containing simple value
    @ Array @counts list of values, indexed by integers
    % Hash %marks set of values, indexed by strings
    
    $x = ’123’; # $x assigned string "123"
    $y = "123 "; # $y assigned string "123 "
    $z = 123; # $z assigned integer 123
    $i = $x + 1; # $x value converted to integer
    $j = $y + $z; # $y value converted to integer
    $a = $x == $y; # numeric compare $x,$y (true)
    $b = $x eq $y; # string compare $x,$y (false)
    $c = $x.$y; # concat $x,$y (explicit)
    $c = "$x$y"; # concat $x,$y (interpolation)
    
## Logical Operators

    Operation Example Meaning
    And     x && y false if x is false, otherwise y
    Or      x || y true if x is true, otherwise y
    Not     ! x true if x is not true, false otherwise
    And     x and y false if x is false, otherwise y
    Or      x or y true if x is true, otherwise y
    Not     not x true if x is not true, false otherwise
    
    open FILE, ’<’, "a" or die "Can’t open a: $!";

## Stream Handles
    $line = <IN>; # read next line from stream IN
    
    print STDOUT "Enter your a number: ";
    $number = <STDIN>;
    if (number < 0) {
        print STDERR "bad number\n";
    }

## Reading and Writing a File: Example

    open OUT, ’>’, ’a.txt’ or die "Can’t open a.txt: $!";
    print OUT "42\n";
    close OUT;
    open IN, ’<’, ’a.txt’ or die "Can’t open a.txt: $!";
    $answer = <IN>;
    close IN;
    print "$answer\n"; # prints 42
    
    
    open my $output, ’>’, ’answer’ or die "Can’t open ...";
    print $output "42\n";
    close $output;
    open my $input, ’<’, ’answer’ or die "Can’t open ...";
    $answer = <$input>;
    close $input;
    print "$answer\n"; # prints 42


## <> give Unix Filter behavior

    while ($line = <>) {
        print $line;
    }
    
## Control Structures
    $x = 1;
    print "Hello";
    
    if ($x > 9999) {
        print "x is big\n";
    }
    
    
## Function Calls
    func(arg{1}, arg{2}, ... arg{n})；
    
## Control Structures
    Example (compute pow = k的n次方):
    # Method 1 ... while
    $pow = $i = 1;
    while ($i <= $n) {
        $pow = $pow * $k;
        $i++;
    }
    
    $pow = 1;
    for ($i = 1; $i <= $n; $i++) {
        $pow *= $k;
    }
    
    $pow = 1;
    foreach $i (1..$n) {
        $pow *= $k;
    }
    
    # Method 4 ... foreach $_
    $pow = 1;
    foreach (1..$n) { $pow *= $k; }
    
    $pow = $k ** $n;
    
## Terminating
    if (! -r "myFile") {
        die "Can’t read myFile: $!\n";
    }
    # or
    die "Can’t read myFile: $!\n" if ! -r "myFile";
    # or
    -r "myFile" or die "Can’t read myFile: $!\n"
    
## Perl and External Commands
    $files = ‘ls $d‘; # output captured
    $exit_status = system "ls $d"; # output to stdout
    open my $files, ’-|’, "ls $d"; # output to stream
    while (<$files>) {
        chomp;
        @fields = split; # split words in $_ to @_
        print "Next file is $fields[$#fields]\n";
    }
    
## File Test Operators
    -r, -w, -x file is readable, writeable, executable
    -e, -z, -s file exists, has zero size, has non-zero size
    -f, -d, -l file is a plain file, directory, sym link
    
    -r "dataFile" && open my $data, ’<’, "dataFile";
    
## Special Variables

    $_ default input and pattern match
    @ARGV list (array) of command line arguments
    $0 name of file containing executing Perl script (cf. shell)
    $i matching string for i
    th regexp in pattern
    $! last error from system call such as open
    $. line number for input file stream
    $/ line separator, none if undefined
    $$ process number of executing Perl script (cf. shell)
    %ENV lookup table of environment variables
    
    
    for ($i = 0; $i < @ARGV; $i++) {
        print "$ARGV[$i] ";
    }
    print "\n";
    
    foreach $arg (@ARGV) {
        print "$arg ";
    }
    print "\n";
    
    print "@ARGV\n";