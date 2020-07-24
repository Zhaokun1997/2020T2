#!/usr/bin/perl -w

use strict;
# use experimental 'smartmatch';
use List::Util qw(max min);

sub match_head 
{
    my ($line) = @_;
    if ($line =~ /^#!.*/)  # match head
    {
        print "#!/usr/bin/perl -w\n";
    }
}

sub match_empty_line
{
    my ($line) = @_;
    if ($line =~ /^$/)
    {
        print "\n";
    }
}

sub match_echo 
{
    my ($line) = @_;
    if ($line =~ /^echo (.*)/)  # match head
    {
        my $echo_content = $1;
        $echo_content =~ s/^'(.*)'/$1/;
        $echo_content =~ s/^"(.*)"/$1/;
        print "print \"$echo_content\\n\";\n";
    }
    elsif ($line =~ /^(\s+)echo (.*)/)
    {
        my $indent = $1;
        my $echo_content = $2;
        $echo_content =~ s/^'(.*)'/$2/;  # if content surounded by "" or ''
        $echo_content =~ s/^"(.*)"/$2/;
        print "$indent", "print \"$echo_content\\n\";\n";
    }
}

sub match_ls_pwd_id_date
{
    my ($line) = @_;
    if ($line =~ /^((ls|pwd|id|date).*)/)  # match (ls|pwd|id|date)
    {
        my $ls_content = $1;
        print "system \"$1\";\n";
    }
}

sub match_var_assign
{
    my ($line) = @_;
    if ($line =~ /^(\w+)=(.*)/)  # match variable assignment
    {
        my $var_name = $1;
        my $var_value = $2;
        print "\$$var_name = '$var_value';\n";
    }
}

sub match_cd
{
    my ($line) = @_;
    if ($line =~ /^cd (.*)/)  # match cd
    {
        my $cd_content = $1;
        print "chdir '$cd_content';\n";
    }
}

sub match_exit
{
    my ($line) = @_;
    if ($line =~ /^exit (.*)/)  # match head
    {
        my $exit_code = $1;
        print "exit $exit_code;\n";
    }
    elsif ($line =~ /^(\s+)exit (.*)/)
    {
        my $indent = $1;
        my $exit_code = $2;
        print "$indent", "exit $exit_code;\n";
    }
}

sub match_read
{
    my ($line) = @_;
    if ($line =~ /^read (.*)/)  # match head
    {
        my $read_content = $1;
        print "\$$read_content = <STDIN>;\n";
        print "chomp \$$line;\n";
    }
    elsif ($line =~ /^(\s+)read (.*)/)
    {
        my $indent = $1;
        my $read_content = $2;
        print "$indent", "\$$read_content = <STDIN>;\n";
        print "$indent", "chomp \$$read_content;\n";
    }
}


sub match_for_loop
{
    my ($line) = @_;
    if ($line =~ /^for (\w+) in ([\d\w\s]+)/)  # match for loop
    {
        # convert for head
        my $var_name = $1;
        my $var_list = $2;
        my @elements = split /\s/, $var_list;
        print "foreach \$$var_name (";
        my $text = "";
        foreach my $e (@elements)
        {
            $text .= "'$e', ";
        }
        $text =~ s/, $//;
        print "$text) {\n";

        # until now, we done with for head, then convert for loop inside
        $line = <>;  # skip "do" statement
        while ($line = <>)
        {
            last if $line =~ /done/;
            match_empty_line($line);
            match_echo($line);
            match_ls_pwd_id_date($line);
            match_var_assign($line);
            match_cd($line);
            match_exit($line);
            match_read($line);
        }
        print "}\n";
    }
    elsif ($line =~ /^for (\w+) in (\*.*)/)
    {
        # convert for head
        my $var_name = $1;
        my $var_list = $2;
        print "foreach \$$var_name (";
        my $text = "glob(\"$var_list\")";
        print "$text) {\n";

        while ($line = <>)
        {
            last if $line =~ /done/;
            match_empty_line($line);
            match_echo($line);
            match_ls_pwd_id_date($line);
            match_var_assign($line);
            match_cd($line);
            match_exit($line);
            match_read($line);
        }
        print "}\n";
    }
}
    


# read from command line or STDIN
while(my $line = <>)
{
    # head
    match_head($line);

    match_empty_line($line);
    match_echo($line);
    match_ls_pwd_id_date($line);
    match_var_assign($line);
    match_cd($line);
    match_exit($line);
    match_read($line);

    # for loop
    match_for_loop($line);
}