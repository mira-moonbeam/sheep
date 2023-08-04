#!/bin/dash

# VARIABLE SUBSTITUTION and COMMENT tests

w=1                             # simple assign
x=COMP204$w                     # cooler simple substitute
y="doublequote 'sub', x = $w"     # In quotes
z='singlequotes "sub" x = $w'
nested_double="nest x = $x"         # nested
nested_raw=single$nested_double     # and again

# This one is my white whale, I just can't get it
echo $z