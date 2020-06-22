## Shell 变量定义的方式
    # 特别注意，中间没有空格
    x=5
    y="6"
    z=abc

## Shell的变量运算
    # 输出内容
    echo $(( $x + $y ))
    # 计算赋值
    # x没有$符号
    x=$(( $x + $y ))
    
## Shell 格式化输出
    x=1
    echo $x
    echo "$x"
    echo " the x value is $x"

## Shell脚本的参数传入
    $0 the name of the command
    $1 the first command-line argument
    $2 the second command-line argument
    $3 the third command-line argument
    $# count of command-line arguments
    $* all of the command-line arguments (together)
    $@ all of the command-line arguments (separately)
    $? exit status of the most recent command
    $$ process ID of this shell
    
## 脚本参数支持正则表达式
    • * matches zero or more of any character
    • ? matches any one character
    • [] matches any one character between the []
    
## Quoting
    Quoting can be used for three purposes in the shell:
    • to group a sequence of words into a single "word"
    • to control the kinds of transformations that are performed
    • to capture the output of commands (back-quotes)
    The three different kinds of quotes have three different effects:
    single-quote (’) grouping, turns off all transformations
    double-quote (") grouping, no transformations except $ and ‘
    backquote (‘) no grouping, capture command results
## Quoting
    Single-quotes are useful to pass shell meta-characters in args: 
        e.g.grep ’S.*[0-9]+$’ < myfile
    Use double-quotes to
        • construct strings using the values of shell variables
            e.g. "x=$x, y=$y" like Java’s ("x=" + x + ", y=" + y)
        • prevent empty variables from "vanishing"
            e.g. use test "$x" = "abc" rather than test $x = "abc" in case $x is empty
        • for values obtained from the command line or a user
            e.g. use test -f "$1" rather than test -f $1 in case
    $1 contains a path with spaces e.g. C:/Program Files/app/data

## Back-quotes
    Back-quotes capture the output of commands as shell values.
    For ‘Command‘, the shell:
    1. performs variable-substitution (as for double-quotes)
    2. executes the resulting command and arguments
    3. captures the standard output from the command
    4. converts it to a single string
    5. uses this string as the value of the expression
    
    Example: convert GIF files to PNG format.
    Original and converted files share the same prefix
    (e.g. /x/y/abc.gif is converted to /x/y/abc.png)
    
```shell script
    #!/bin/sh
    # ungif - convert gifs to PNG format
    for f in "$@"
    do
        dir=‘dirname "$f"‘
        prefix=‘basename "$f" .gif‘
        outfile="$dir/$prefix.png"
        giftopnm "$f" | pnmtopng > "$outfile"
    done
```

## Testing
    
    The test command performs a test or combination of tests and:
    • returns a zero exit status if the test succeeds
    • returns a non-zero exit status if the test fails
    Provides a variety of useful testing features:
    • string comparison ( = != )
    • numeric comparison ( -eq -ne -lt )
    • checks on files ( -f -x -r )
    • boolean operators ( -a -o ! )

    https://www.runoob.com/linux/linux-shell-test.html
    
## IF 语句
    if [ -r $HOME ] # neater than: if test -r $HOME
    then
        echo "$0: $HOME is readable"
    fi
    # Test whether a user exists in passwd file
    if grep "^$user" /etc/passwd > /dev/null
    then
        # do something if they do exist ...
    else
        echo "$0: $user does not exist"
    fi
    
## LOOP COMMANDS
    sum=0
    for n in "$@" # use "$@" to preserve args
    do
        sum=‘expr $sum + "$n"‘
    done
    # Process files in $PWD, asking for confirmation
    for file in *
    do
        echo -n "Process $file? "
        read answer
        case "$answer" in
            [yY]*) process < $file >> results ;;
            *) ;;
        esac
    done
    
## 更多代码讲解

```shell script
    if (($# == 1))
    then
        start=1
        finish=$1
    elif (($# == 2))
    then
        start=$1
        finish=$2
    else
        echo "Usage: $0 <start> <finish>" 1>&2
        exit 1
    fi
```
    
```shell script
    if ! [[ "$argument" =~ ^-?[0-9]+$ ]]
    then
        echo "$0: argument '$argument' is not an integer" 1>&2
        exit 1
    fi
```
    
```shell script
    if diff -i -w "$file1" "$file2" >/dev/null
    then
        echo "$file1 is a copy of $file2"
    fi
```

```shell script
    # C格式
    for((i=1;i<=5;i++))
    do
        echo abc
    done
    
    # seq函数
    for i in $(seq 5)
    do
        echo abc
    done
    
    # ls函数
    for i in `ls` #ls表示当前目录的文件数
    do
        echo abc
    done
    
    # {x..y}
    for i in {1..5}
    do
        echo abc
    done
    
    # stringchar {x..y}
    for i in stringchar {1..5}
    do
        echo abc
    done
    
    # 直接列出来。。。
    for i in 1 2 3 4 5
    do
        echo abc
    done
```

```shell script
    index=1
    while test $index -le $n_path_components
    do
        directory=`echo "$PATH"|cut -d: -f$index`
        f="$directory/$program"
        if test -x "$f"
        then
            ls -ld "$f"
            program_found=1
        fi
        index=`expr $index + 1`
    done

    # 双小括号
    number=5
    while ((number > 0))
    do
         echo abc
         number=$((number - 1))
    done
    
    # 单中括号
    number=5
    while [ $number -gt 0 ]
    do
         echo abc
         number=$((number - 1))
    done
    
    # 双中括号
    number=5
    while [[ $number -gt 0 ]]
    do
         echo abc
         number=$((number - 1))
    done
    
    # test函数
    number=5
    while test $number -gt 0
    do
         echo abc
         number=$((number - 1))
    done
```

* 单中括号 [ ]  a. [ ] 两个符号左右都要有空格分隔  b. 内部操作符与操作变量之间要有空格：如 [“a” = “b” ]  c. 字符串比较中，> < 需要写成> \< 进行转义  d. [ ] 中字符串或者${}变量尽量使用”” 双引号扩住，以避免值未定义引用而出错  e. [ ] 中可以使用 –a –o 进行逻辑运算  f. [ ] 是bash 内置命令：[ is a shell builtin  双中括号  a. [[ ]] 两个符号左右都要有空格分隔  b. 内部操作符与操作变量之间要有空格：如 [[ “a’ = “b” ]]  c. 字符串比较中，可以直接使用 > < 无需转义  d. [[ ]] 中字符串或者${}变量尽量使用”” 双引号扩住，如未使用”“会进行模式和元字符匹配  e. [[ ]] 内部可以使用 && || 进行逻辑运算  f. [[ ]] 是bash keyword：[[ is a shell keyword

