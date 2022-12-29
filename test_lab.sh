#!/bin/bash

ROOT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

for i in {1..15}
do
    echo "#################################################################################################"
    echo "Test $i"
    res=$(python3 SemantickiAnalizator.py < $ROOT_DIR/testovi/test_$i/test.in | diff $ROOT_DIR/testovi/test_$i/test.out -)
    if [ "$res" != "" ]
    then
        echo "FAIL"
        echo $res
    else
        echo "OK"
    fi
done
