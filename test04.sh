#!/bin/dash

for i in 1 2 3
do
    echo $i
done

for word in this is a string
do
    echo $word
    for i in 1 2 3
    do
        echo $i
    done
done

for file in *.c
do
    echo $file
done