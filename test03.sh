#!/bin/dash

# EXIT and CHANGEDIR tests (From SPEC)

echo *
cd /tmp
echo *
cd ..
echo *

echo hello world
exit
echo this will not be printed
exit 0
echo this will double not be printed
exit 3