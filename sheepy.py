#! /usr/bin/env python3

import sys
import re

filepath = sys.argv[1]

# * HANDLER HELPERS
def remove_unescaped_quotes(s):
    return re.sub(r'(?<!\\)(\'|")', '', s)

def check_var_sub(line):
    # enclosed by "" translate, otherwise enclosed by '' keep literal
    if re.search('\$\w+', line):
        line = re.sub(r'\$(\w+)', r'{\1}', line)
        for match in re.findall(r"'([^']*)'", line):
                # Within those substrings, replace {var} back into $var.
                replaced = re.sub(r'\{(\w+)\}', r'$\1', match)

                # Replace the original substring with the modified one.
                line = line.replace("'" + match + "'", "'" + replaced + "'")

        line = remove_unescaped_quotes(line)
        return 'f"' + line + '"'
    else:
        line = remove_unescaped_quotes(line)
        return '"' + line + '"'

# *HANDLERS
def echo_line(line):
    line = line.replace('echo ', '', 1)

    str_to_print = ""
    if line.startswith(("'", '"')) and line.endswith(("'", '"')):       
        str_to_print = line
    else:
        wordarr = re.split('\s+', line)
        for word in wordarr:
            str_to_print += word + " "
        str_to_print = str_to_print.strip()

    str_to_print = check_var_sub(str_to_print)
    return f'print({str_to_print})'

def var_assign(line):
    var, value = re.split('=', line)
    if value.startswith(("'", '"')) and value.endswith(("'", '"')):
        value = value[1:-1]
    
    value = check_var_sub(value)
    return f'{var} = {value}'

command_handler = {
    # Match enclosed quotes \'[^\']*\' | \"[^\"]*\"
    # Match any string of allowed characters without quotes or variable subs \$\w+ | \w+
    # Match zero or more whitespace to allow space (patterns)\s*
    r'^echo ((\'[^\']*\'|\"[^\"]*\"|\$\w+|\w+)\s*)+$': echo_line,
    r'^[\w]+=((\'[^\']*\'|\"[^\"]*\"|\$\w+|\w+)\s*)+$': var_assign
}
with open(filepath, 'r') as file:
    lines = file.readlines()

for line in lines:
    line = line.strip()

    for pattern, handler in command_handler.items():
        if re.match(pattern, line):
            print(handler(line))
            break
    else:
        print()