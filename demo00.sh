#!/bin/dash

# Print a list of files in the current directory

echo "Listing files in the current directory:"
for file in *
do
    echo $file
done

exit 0
