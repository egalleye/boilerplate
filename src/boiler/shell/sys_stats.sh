#!/bin/bash

onehundred="100"
re='^[0-9]+$'


while [ 1 ] 
do
    disc_usage=$(sh disc_stats.sh);
    cpu_usage=$(sh cpu_stats.sh);
    if [ -z $cpu_usage ]; then
        continue;
    fi
    echo "cpu_usage, disk_usage"
    echo "$cpu_usage, $disc_usage"
    echo "cpu_usage, disk_usage" > /usr/share/nginx/html/sys_stats.csv
    echo "$cpu_usage, $disc_usage" >> /usr/share/nginx/html/sys_stats.csv
    sleep 1
done
