#!/bin/bash

onehundred="100"
cpu_usage=$(top -b -n2 -d0.01 | awk '/^top/{i++}i==2' |  grep --line-buffered "Cpu(s)" | awk '{print $8}')
idstr="id,"

if [ "$cpu_usage" == "$idstr" ]; then
    exit 1;
fi

cu=$(bc <<< "$onehundred-$cpu_usage")

echo "$cu"
