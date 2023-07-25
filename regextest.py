import re

line = 'test[ing] is * fun ? I love [AI]'

# Pattern matches any word that contains your special characters
pattern = r'(?:^|\s)(\S*[\*\?\[\]]+\S*)(?:\s|$)'
matches = re.findall(pattern, line)

print(matches) # it will print ['test[ing]', '[AI]']
