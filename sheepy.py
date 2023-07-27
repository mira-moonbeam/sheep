#! /usr/bin/env python3
import sys
import re

# TODO: SHEBANG LINE

#* File structure
# sheepy.py (command_handler and fileread. Import all the functions in command handler)
# subset_0.py (handlers and helpers for subset 0)
# subset_1.py (take a guess)

# * HANDLER HELPERS
def remove_start_end_quotes(s):
    if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
        return s[1:-1]
    else:
        return s

# *HANDLERS

# SUBSET 0
# $
def var_sub(variables, line):
    no_single_quotes = re.sub(r"'[^']*'", "", line)  # remove all parts within single quotes
    matches = re.findall(r"\$\w+", no_single_quotes)  # find all $words in the remaining part
    
    for match in matches:       
        varName = match[1:]
        line = line.replace(match, variables[varName])

    return line 

# echo
def echo_line(variables, line):
    line = line.replace('echo ', '', 1)

    str_to_print = ""
    if line.startswith(("'")) and line.endswith(("'")):       
        str_to_print = line

    else:
        wordarr = re.split('\s+', line)
        for word in wordarr:
            str_to_print += word + " "
        str_to_print = str_to_print.strip()

    str_to_print = var_sub(variables, str_to_print)
    str_to_print = remove_start_end_quotes(str_to_print)
    return f'print("{str_to_print}")'

# =
def var_assign(variables, line):
    
    var, value = re.split('=', line)

    if variables:
        value = var_sub(variables, value)

    value = remove_start_end_quotes(value)

    variables[var] = value
    return f'{var} = "{value}"'

# #
def inline_comments(line):
    pattern = r'(.*) #(.*)$'

    # Search for the pattern in the line
    match = re.search(pattern, line)

    if match:
        content = match.group(1)
        comment = "# " + match.group(2)
        return content, comment
    else:
        return line, ""

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
        if line == '#!/bin/dash':
            line = '#!/usr/bin/python3 -u'
        print(line)
