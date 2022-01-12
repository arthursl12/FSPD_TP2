#!/bin/bash

set -eu

TEST_DIR="tests"

rm -rf $TEST_DIR/out*.txt
for N in $(seq 1 3); do 
    tmux split-pane -v -c $(pwd)/ make run_serv_pares_1 arg=8888
    sleep .5 
    make run_cli_pares arg=localhost:8888 < $TEST_DIR/test$N.txt > $TEST_DIR/output$N.txt
    if [[ "$N" -eq 3 ]]; then
        echo "N==3"
        make run_cli_pares arg=localhost:8888 < $TEST_DIR/test3.1.txt > $TEST_DIR/output3.1.txt
    fi

    if ! diff $TEST_DIR/output$N.txt $TEST_DIR/true$N.txt > /dev/null ; then
        if [[ "$N" -eq 3 ]]; then
            if ! diff $TEST_DIR/output3.1.txt $TEST_DIR/true3.1.txt > /dev/null ; then
                echo "test$N failed"
                exit 1
            fi
        fi
        echo "test$N failed"
        exit 1
    fi
    echo "test$N passed"
done


tmux splitw -v -c $(pwd)/ make run_serv_pares_2 arg=5555
sleep .5
make run_cli_pares arg=localhost:5555 < $TEST_DIR/test4.txt > $TEST_DIR/output4.txt
tmux splitw -v -c $(pwd)/ make run_serv_central arg=6666
sleep .5
make run_cli_pares arg=localhost:5555 < $TEST_DIR/test5.txt > $TEST_DIR/output5.txt
make run_cli_central arg=localhost:6666 < $TEST_DIR/test6.txt > $TEST_DIR/output6.txt
tmux splitw -v -c $(pwd)/ make run_serv_pares_2 arg=7777
sleep .5
make run_cli_pares arg=localhost:7777 < $TEST_DIR/test9.txt > $TEST_DIR/output9.txt
make run_cli_central arg=localhost:6666 < $TEST_DIR/test7.txt > $TEST_DIR/output7.txt
make run_cli_pares arg=localhost:5555 < $TEST_DIR/test8.txt > $TEST_DIR/output8.txt
make run_cli_pares arg=localhost:7777 < $TEST_DIR/test10.txt > $TEST_DIR/output10.txt

tmux splitw -v -c $(pwd)/ make run_serv_central arg=8888
sleep .5
make run_cli_pares arg=localhost:5555 < $TEST_DIR/test11.txt > $TEST_DIR/output11.txt
make run_cli_pares arg=localhost:7777 < $TEST_DIR/test12.txt > $TEST_DIR/output12.txt
make run_cli_central arg=localhost:8888 < $TEST_DIR/test13.txt > $TEST_DIR/output13.txt
make run_cli_pares arg=localhost:5555 < $TEST_DIR/test14.txt > $TEST_DIR/output14.txt
make run_cli_pares arg=localhost:7777 < $TEST_DIR/test15.txt > $TEST_DIR/output15.txt


for N in $(seq 4 13); do 
    if ! diff $TEST_DIR/output$N.txt $TEST_DIR/true$N.txt > /dev/null ; then
        echo "test$N failed"
        exit 1
    fi
    echo "test$N passed"
done