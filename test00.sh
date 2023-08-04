#!/bin/dash

# ECHO and VARIABLE ASSIGNMENT tests

w=1
x=COMP204$w
y='in         "single  quotes" i dont $x'
z="double quotes          'with' spaces         $w"

echo long            long                            space
echo '.*()           ""     $@$   &'
echo "okay now with    and a long space usi      '     ng 'double quotes"