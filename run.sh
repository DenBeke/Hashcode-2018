#!/bin/sh

for f in input/*.in
do
    name=$(basename $f .in)
    echo "Processing $name"
    python3 main.py < input/$name.in > output/$name.out&
done
while ps aux | grep python3 | grep -v grep |  wc -l ; do sleep 1; done
