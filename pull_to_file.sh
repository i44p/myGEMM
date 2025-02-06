#!/bin/sh

END=20

for i in $(seq 1 $END); do 
    echo [$i/$END];
    python3 pull_data.py ENABLE_CUDA=0 >> data.csv
done
