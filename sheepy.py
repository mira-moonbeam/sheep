#! /usr/bin/env python3
import tempfile
import os
import sys
import re

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
    no_end_quote = False
    no_start_quote = False

    for match in matches:       
        varName = match[1:]
        if bool(re.match('^loopvar:.+$', variables[varName])):
            if line == ("$" + varName):
                # ONLY
                line = line.replace(match, varName)
                no_end_quote = True
                no_start_quote = True
            elif line.startswith(("$" + varName)):
                # STARTS
                line = line.replace(match, varName + " + \"")
                no_start_quote = True
            elif line.endswith(("$" + varName)):
                # ENDS
                line = line.replace(match, "\" + " + varName)
                no_end_quote = True
            else:
                #MIDDLE
                line = line.replace(match, "\" + " + varName + " + \"")
        else:
            line = line.replace(match, variables[varName])

    return {'line': line, 'end': no_end_quote, 'start': no_start_quote}

# echo
def echo_line(variables, line, *args, **kwargs):
    line = line.replace('echo ', '', 1)
    no_end_quote = False
    no_start_quote = False
    str_to_print = ""
    if line.startswith(("'")) and line.endswith(("'")):       
        str_to_print = line

    else:
        wordarr = re.split('\s+', line)
        for word in wordarr:
            str_to_print += word + " "
        str_to_print = str_to_print.strip()

    # VARIABLE SUBSTITUTION

    results = var_sub(variables, str_to_print)
    str_to_print = results['line']
    no_end_quote = results['end']
    no_start_quote = results['start']

    # GLOBBING


    globs = behold_the_glob(str_to_print)
    # given gjealk glob DLKfkj
    # replace glob at start with glob + "rest of string"
    # replace glob at end with "rest of string" + glob
    # replace glob at middle with "first" + glob + "Seoncd"
    # replace glob at start and end with glob
    for key in globs.keys():
        replacement = globs[key]
        if str_to_print == key:
            # ONLY
            str_to_print = str_to_print.replace(key, replacement)
            no_end_quote = True
            no_start_quote = True
        elif str_to_print.startswith(key):
            # STARTS
            str_to_print = str_to_print.replace(key, replacement + " + \"")
            no_start_quote = True
        elif str_to_print.endswith(key):
            # ENDS
            str_to_print = str_to_print.replace(key, "\" + " + replacement)
            no_end_quote = True
        else:
            #MIDDLE
            str_to_print = str_to_print.replace(key, "\" + " + replacement + " + \"")
    
    end_quote = "" if no_end_quote else "\""
    start_quote = "" if no_start_quote else "\""
    str_to_print = remove_start_end_quotes(str_to_print) 
    return f'print({start_quote}{str_to_print}{end_quote})'

# =
def var_assign(variables, line, *args, **kwargs):
    
    var, value = re.split('=', line)

    if variables:
        results = var_sub(variables, value)
        value = results['line']
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
    
# SUBSET 1, where i realized variables and stuff can just be called without calling but it's too late
# globbing
def behold_the_glob(line):
    # look for word containing *, ?, [, and ]
    # return word: replacement
    # go replace it and deal with it in the adult function
    result=  {}
    pattern = r'(?:^|\s)(\S*[\*\?\[\]]+\S*)(?:\s|$)'

    # Look for matches in the line
    no_single_quotes = re.sub(r"'[^']*'", "", line)  # remove all parts within single quotes
    matches = re.findall(pattern, no_single_quotes)

    if len(matches) > 0:
        imports.add("glob")

    # For each match, replace it appropriately
    for match in matches:
        result[match] = f'"".join(sorted(glob.glob("{match}")))'

    return result

def for_loop(variables, start_line, depth, *args, **kwargs):
    loop_variables = variables.copy()
    indent_level = '\t' * depth
    pattern = r'for\s+(\w+)\s+in\s+(.*)'

    match = re.match(pattern, start_line)
    if match:
        variable_name = match.group(1)
        values = match.group(2)
        loop_variables[variable_name] = "loopvar:"+variable_name
    else:
        return "Unrecognized command"

    loop_values = behold_the_glob(values)
    if not loop_values:
        values = re.split(' ', values)
        loop_values = "["
        for value in values:
            loop_values += f'"{value}",'
        loop_values = loop_values[:-1] + "]"
    else:
        loop_values = list(loop_values.values())[0]
        loop_values = re.split('\(', loop_values, 1)
        loop_values = loop_values[1][:-1]
    
    temp.write(indent_level + f'for {variable_name} in {loop_values}:' + '\n')

    for line in file:
        line = line.strip()
        if line == "done":
            return ""

        for pattern, handler in command_handler.items():
            if re.match(pattern, line):
                print_line = handler(loop_variables, line, depth + 1) + comment
                temp.write(indent_level +'\t' + print_line + '\n')
                break
        else:
            if line != "do":
                temp.write(indent_level +'\t' + line + '\n')

    return

def exit_handle(variables, line, *args, **kwargs):
    imports.add("sys")
    line = re.split(' ', line)

    if len(line) == 1:
        return "sys.exit()"
    else:
        return f'sys.exit({line[1]})'
    
# *COMMAND HANDLER
filepath = sys.argv[1]
command_handler = {
    # Match enclosed quotes \'[^\']*\' | \"[^\"]*\"
    # Match any string of allowed characters without quotes or variable subs \$\w+ | \w+
    # Match zero or more whitespace to allow space (patterns)\s*
    #r'^echo ((\'[^\']*\'|\"[^\"]*\"|\$\w+|\w+|#)\s*)+$': echo_line,
    #r'^[\w]+=((\'[^\']*\'|\"[^\"]*\"|\$\w+|\w+|#)\s*)+$': var_assign

    r'^echo .+$': echo_line,
    r'^[\w]+=.+': var_assign,
    r'^for \w+ in .*': for_loop,
    r'^exit\s*[0-9]*$': exit_handle,
}

# *MAIN LOOP
temp = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
imports = set()
variables = {}


with open(filepath, 'r') as file:
    for line in file:
        line = line.strip()
        line, comment = inline_comments(line)

        for pattern, handler in command_handler.items():
            if re.match(pattern, line):
                print_line = handler(variables, line, depth=0) + comment
                temp.write(print_line + '\n')  # Write to temporary file instead of printing
                break
        else:
            if line != '#!/bin/dash':
                temp.write(line + '\n')

# Close the temporary file
temp.close()

# Now print the imports
print('#!/usr/bin/python3 -u')
print()
for imp in imports:
    print(f'import {imp}')

# Now read from the temporary file and print its content
with open(temp.name, 'r') as file:
    for line in file:
        print(line, end='')

# Remove the temporary file
os.remove(temp.name)