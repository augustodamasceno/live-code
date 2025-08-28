#!/bin/bash
# Run all Python scripts in the current directory 
# and save their output to Markdown files

for script in *.py; do
    if [[ -f "$script" ]]; then
        out="${script%.py}.md"
        python3 "$script" > "$out" 2>&1
    fi
done