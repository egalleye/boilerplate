#!/bin/bash

cpu_usage=$(grep 'cpu ' /proc/stat | awk '{cpu_usage=($2+$4)*100/($2+$4+$5)} END {print cpu_usage}')
echo "CPU usage (%)" > cpu_usage.out 
echo "$cpu_usage" >> cpu_usage.out
