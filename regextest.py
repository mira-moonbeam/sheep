import re

variables = {'x': '1', 'y': 'lots of $x cash', 'z': 'COMP20411', 'w': 'butlots of $x cash'}
line = 'print($x $y $z $w)'
print(variables)


no_single_quotes = re.sub(r"'[^']*'", "", line)  # remove all parts within single quotes
matches = re.findall(r"\$\w+", no_single_quotes)  # find all $words in the remaining part
for match in matches:    
    print(line) 
    varName = match[1:]
    line = line.replace(match, variables[varName])

print(line)