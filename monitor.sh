#!/bin/bash


# start tcpdump
if [ "$1" == "start" ]; then
    sudo tcpdump -i $(ip addr | grep 'inet 10.10' | awk '{print $NF}') | awk '{gsub("-link-.*", "", $3); gsub("-link-.*", "", $5); if ($NF != 0) print $1, $3, $5, $NF}' > monitor_log
    # echo "tcpdump started"
elif [ "$1" == "stop" ]; then
    sudo kill $(ps aux | grep 'sudo tcpdump -i' | awk '{print $2}')
    echo "tcpdump stopped"
    exit
else
    echo "invalid input"
fi
