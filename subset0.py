#! /usr/bin/env python3
import re

# TODO: SHEBANG LINE
# TODO: when using a module, add to a list of import statements we need to use like glob
# TODO: IN GLOB HANDLER: get the dang quotes working like "thing" + globglob


# SUBSET 0
# echo, =, $, #

# * HANDLER HELPERS
def remove_start_end_quotes(s):
    if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
        return s[1:-1]
    else:
        return s

# *HANDLERS
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
