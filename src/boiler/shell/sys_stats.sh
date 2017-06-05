#!/bin/bash

onehundred="100"
re='^[0-9]+$'


while [ 1 ] 
do
    disc_usage=$(bash disc_stats.sh);
    cpu_usage=$(bash cpu_stats.sh);
    mem_usage=$(bash mem_stats.sh);
    if [ -z $cpu_usage ]; then
        continue;
    fi
    echo "cpu_usage, disk_usage, mem_usage"
    echo "$cpu_usage, $disc_usage, $mem_usage"
    ## Echo in header
    #echo "cpu_usage, disk_usage" > /usr/share/nginx/html/sys_stats.csv
    echo "cpu_usage, disk_usage, mem_usage" > /var/www/html/sys_stats.csv
    #echo "cpu_usage, disk_usage"
    ## Echo in rows 
    #echo "$cpu_usage, $disc_usage" >> /usr/share/nginx/html/sys_stats.csv
    echo "$cpu_usage, $disc_usage, $mem_usage" >> /var/www/html/sys_stats.csv
    #echo "$cpu_usage, $disc_usage"


    ## Uncomment this to turn on python logging to db
    #python3 sysstat_insert.py
    sleep 1
done
