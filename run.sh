#!/bin/sh

for f in input/*.in
do
    name=$(basename $f .in)
    echo "Processing $name"
    python3 main.py < input/$name.in > output/$name.out&
done

while [ $(echo $(ps aux | grep python3) | wc -l) -gt 1 ]; do sleep 1; done