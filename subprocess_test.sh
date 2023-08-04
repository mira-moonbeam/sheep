#!/bin/dash


var=testdir
mkdir $var
touch test_file.txt
ls -l test_file.txt

for course in COMP1511 COMP1521 COMP2511 COMP2521 # keyword
do                                                # keyword
    echo $course                                  # builtin
    mkdir $course                                 # external command
    chmod 700 $course                             # external command
done          