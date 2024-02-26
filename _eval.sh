#!/bin/bash

inputFile="test_cases.dat"

while IFS= read -r line
do
    output=$(./runner "$line" 2>&1)
    exitCode=$?

    if [ $exitCode -eq 0 ]; then
        echo "{\"result\": \"success\", \"value\": \"$output\"}"
    else
        echo "{\"result\": \"failure\", \"output\": \"$output\"}"
    fi
done < "$inputFile"
