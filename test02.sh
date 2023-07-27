#!/bin/dash

# VARIABLE ASSIGNMENT AND VARIABLE ACCESS TEST

# Simple Assign
x=1
y='lots of $x cash'

# Substitution
z=COMP2041$x

# Nested Substitution
w="but$y"

echo $x $y $z $w