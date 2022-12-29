#!/bin/bash

ROOT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

for i in {1..15}
do
    echo "#################################################################################################"
    echo "Test $i"
    ASSERT="$(diff -B <(python3 SemantickiAnalizator.py < $ROOT_DIR/testovi/test_$i/test.in) <(cat $ROOT_DIR/testovi/test_$i/test.out))"
    # if ASSERT is empty write OK
    if [ -z "$ASSERT" ]; then
      echo "OK"
    else
      echo $ASSERT
    fi
done
