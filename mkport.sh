#!/bin/bash

make_port(){
    echo "create ports for serial read write"
    sleep 1
    socat -d -d pty,raw,echo=0 pty,raw,echo=0 > ports.txt 2>&1
}

make_port