#!/bin/dash

# Demon for loop test

echo "Three-Nested For-loop:"

for i in 1 2 3
do
    echo "Outer Loop: Iteration $i"
    
    for j in 1 2 3
    do
        echo "   Middle Loop: Iteration $j"
        
        for k in 1 2 3
        do
            echo "      Inner Loop: Iteration $k"
        done
    done
done

echo "Script execution completed."
