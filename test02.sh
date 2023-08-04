#!/bin/dash

# GLOBBING and FOR-LOOP tests

echo *

C_files=*.[ch]
echo $C_files

echo middle ?.py glob
echo ?.py start glob
echo end glob ?.py

echo multi ?.py ?.py * glob

x=1
y=2

for word in this is a string
do
    echo "$word combined with other words"

    for i in $x $y
    do
        echo $i
    done
    
    for file in $C_files
    do
        echo $file
    done
done