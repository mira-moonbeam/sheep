#!/bin/dash

# Honestly, I'm just proud of this one so I reused it from tests

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