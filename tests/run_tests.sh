#!/bin/bash

set -eu

TEST_DIR="tests"

rm -rf $TEST_DIR/out*.txt
for N in $(seq 1 3); do 
    tmux split-pane -v -c $(pwd)/ make run_serv_pares_1 arg=8888
    sleep .5 
    make run_cli_pares arg=localhost:8888 < $TEST_DIR/test$N.txt > $TEST_DIR/output$N.txt
    if ! diff $TEST_DIR/output$N.txt $TEST_DIR/true$N.txt > /dev/null ; then
        echo "test$N failed"
        exit 1
    fi
    echo "test$N passed"
done