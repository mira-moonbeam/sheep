#! /usr/bin/env python3
import re
# TODO: when using a module, add to a list of import statements we need to use like glob
# TODO: IN GLOB HANDLER: get the dang quotes working like "thing" + globglob

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