#!/bin/bash

set -eu

TEST_DIR="tests"

rm -rf $TEST_DIR/out*.txt

tmux split-pane -v -c $(pwd)/ make run_serv_pares_1 arg=8888
sleep .5 
make run_cli_pares arg=localhost:8888 < $TEST_DIR/test01.txt > $TEST_DIR/output1.txt
if ! diff $TEST_DIR/output1.txt $TEST_DIR/true01.txt > /dev/null ; then
    echo "test01 failed"
    exit 1
fi
echo "test01 passed"