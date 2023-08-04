#!/bin/dash

# ECHO and VARIABLE ASSIGNMENT/SUBSTITUTION demo

# Simple Echos
echo hello world # inline

echo long            long                            space with no quotes

# With quotes, double and single
echo '.*()                $@$   &'
echo "okay now with *()    and a long space usi           ng double quotes"

# VARIABLE ASSIGNMENT AND VARIABLE ACCESS TEST

# Simple Assign, single and double quotes
x=1
y='lots of $x cash'

# Substitution
z=COMP204$x

# Nested Substitution
w="but$y"

# And now all of it
echo $x $y$z $w