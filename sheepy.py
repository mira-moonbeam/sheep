#! /usr/bin/env python3
import sys
import re
from subset0 import echo_line, var_assign, inline_comments

#* File structure
# sheepy.py (command_handler and fileread. Import all the functions in command handler)
# subset_0.py (handlers and helpers for subset 0)
# subset_1.py (take a guess)

filepath = sys.argv[1]
command_handler = {
    # Match enclosed quotes \'[^\']*\' | \"[^\"]*\"
    # Match any string of allowed characters without quotes or variable subs \$\w+ | \w+
    # Match zero or more whitespace to allow space (patterns)\s*
    #r'^echo ((\'[^\']*\'|\"[^\"]*\"|\$\w+|\w+|#)\s*)+$': echo_line,
    #r'^[\w]+=((\'[^\']*\'|\"[^\"]*\"|\$\w+|\w+|#)\s*)+$': var_assign

    r'^echo .+$': lambda line: echo_line(variables, line),
    r'^[\w]+=.+': lambda line: var_assign(variables, line)
}

variables = {}

with open(filepath, 'r') as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()
    line, comment = inline_comments(line)

    for pattern, handler in command_handler.items():
        if re.match(pattern, line):
            print_line = handler(line) + comment
            print(print_line)
            break
    else:
        print(line)
