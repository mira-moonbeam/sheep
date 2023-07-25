#! /usr/bin/env python3

import sys
import re

filepath = sys.argv[1]

# TODO: SHEBANG LINE
# TODO: when using a module, add to a list of import statements we need to use like glob
# TODO: IN GLOB HANDLER: get the dang quotes working like "thing" + globglob
# TODO: File structure
# sheepy.py (command_handler and fileread. Import all the functions in command handler)
# subset_0.py (handlers and helpers for subset 0)
# subset_1.py (take a guess)

# * HANDLER HELPERS
def remove_unescaped_quotes(s):
    return re.sub(r'(?<!\\)(\'|")', '', s)

def behold_the_glob(line):
    # look for word containing *, ?, [, and ]

    # replace it with + "".globglob("theSTRING") +
    # Unless it's the start of the line, then just "".globglob("theSTRING") + 
    # OR END, then + "".globglob("theSTRING")
    # if it's alone :( then just "".globglob("theSTRING") will do
    # The regex pattern finds words that contain one of the special characters *, ?, [, ]
    pattern = r'(?:^|\s)(\S*[\*\?\[\]]+\S*)(?:\s|$)'

    # Look for matches in the line
    matches = re.findall(pattern, line)

    # For each match, replace it appropriately
    for match in matches:
        # Check if match is at the start, end, or alone in the line
        if line.startswith(match) and line.endswith(match):
            replacement = f'"".join(sorted(glob.glob("{match}")))'
        elif line.startswith(match):
            replacement = f'"".join(sorted(glob.glob("{match}"))) + "'
        elif line.endswith(match):
            replacement = f'" + "".join(sorted(glob.glob("{match}")))'
        else:
            replacement = f'" + "".join(sorted(glob.glob("{match}"))) + "'

        # Replace the match in the line
        line = line.replace(match, replacement)
        
    return line

def check_var_sub(line):
    # enclosed by "" translate, otherwise enclosed by '' keep literal
    if re.search('\$\w+', line):
        line = re.sub(r'\$(\w+)', r'{\1}', line)
        for match in re.findall(r"'([^']*)'", line):
                # Within those substrings, replace {var} back into $var.
                replaced = re.sub(r'\{(\w+)\}', r'$\1', match)

                # Replace the original substring with the modified one.
                line = line.replace("'" + match + "'", "'" + replaced + "'")

        return 'f' + line 
    else:
        return line 

def inline_comments(line):
    # Idead is to grab the comments (anything past a # that isnt escape charactered)
    # Return it to some temp like line, comments = inline_comments(line)
    # Keep doing on line as usual, then at the end add comment to it
    pattern = r'(.*) #(.*)$'

    # Search for the pattern in the line
    match = re.search(pattern, line)

    if match:
        content = match.group(1)
        comment = match.group(2)
        return content, comment
    else:
        return line, None

# *HANDLERS
def echo_line(line):
    line, comment = inline_comments(line)
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
    str_to_print = remove_unescaped_quotes(str_to_print)
    str_to_print = behold_the_glob(str_to_print)

    if comment:
        return f'print({str_to_print}) #{comment}'
    
    return f'print({str_to_print})'

def var_assign(line):
    line, comment = inline_comments(line)
    var, value = re.split('=', line)
    if value.startswith(("'", '"')) and value.endswith(("'", '"')):
        value = value[1:-1]
    
    value = check_var_sub(value)

    value = remove_unescaped_quotes(value)
    value = behold_the_glob(value)

    if comment:
        return f'{var} = {value} #{comment}'
    
    return f'{var} = {value}'

command_handler = {
    # Match enclosed quotes \'[^\']*\' | \"[^\"]*\"
    # Match any string of allowed characters without quotes or variable subs \$\w+ | \w+
    # Match zero or more whitespace to allow space (patterns)\s*
    #r'^echo ((\'[^\']*\'|\"[^\"]*\"|\$\w+|\w+|#)\s*)+$': echo_line,
    #r'^[\w]+=((\'[^\']*\'|\"[^\"]*\"|\$\w+|\w+|#)\s*)+$': var_assign

    r'^echo .+$': echo_line,
    r'^[\w]+=.+': var_assign
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
        print(line)