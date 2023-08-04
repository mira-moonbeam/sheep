#!/bin/dash

# INPUT and SUBPROCESS tests

echo What is your name:
read name

echo What is your quest:
read quest

echo What is your favourite colour:
read colour

echo What is the airspeed velocity of an unladen swallow:
read velocity

echo Hello $name, my favourite colour is $colour too.

var=testdir
mkdir "$var"
touch test_file.txt
ls -l test_file.txt

for course in COMP1511 COMP1521 COMP2511 COMP2521 # keyword
do                                                # keyword
    echo $course                                  # builtin
    mkdir $course                                 # external command
    chmod 700 $course                             # external command
done          