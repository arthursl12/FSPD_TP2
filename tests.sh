#!/bin/bash

set -eu

rm -rf out*.txt

tmux split-pane -v -c $(pwd)/ make run_serv_pares_1 arg=8888
sleep .5 
make run_cli_pares arg=localhost:8888 < test01.txt > output1.txt
if ! diff output1.txt true01.txt > /dev/null ; then
    echo "test01 failed"
    exit 1
fi
echo "test01 passed"