#!/bin/bash

TIMEOUT=60

cputime=$(cat supermicro_benchmark.config | grep "cputime" | sed -e 's/=/ /g' | awk '{print $2}')

timeunits=$(echo "${cputime: -1}")
TIMEOUT=${cputime::-1}

if [ "$timeunits" == 'S' ] || [ "$timeunits" == 's' ]
then
    timeunitsstr="seconds"
    timeseconds=$TIMEOUT
    echo "sTimeout = $TIMEOUT"
elif [ "$timeunits" == 'M' ] || [ "$timeunits" == 'm' ]
then
    timeunitsstr="minutes"
    timeseconds=$(echo "$TIMEOUT * 60" | bc -l)
    echo "mTimeout = $TIMEOUT"
elif [ "$timeunits" == 'H' ] || [ "$timeunits" == 'h' ]
then
    timeunitsstr="hours"
    timeseconds=$(echo "$TIMEOUT * 3600" | bc -l)
    echo "hTimeout = $TIMEOUT"
else
    echo "No time"
    timeseconds=$TIMEOUT
fi

echo "Running CPU test for $timeseconds seconds"

num_cpus=8
echo "cpu_stress" > ~/supermicro_benchmarks/cpu/cpu_test.txt
prestress=$(uptime | awk '{print $11}' | sed 's/[^0-9.]*//g')
stress -c $num_cpus -i 1 -m 1 --vm-bytes 1024M -t $timeseconds
poststress=$(uptime | awk '{print $11}' | sed 's/[^0-9.]*//g')

echo "Prestress = $prestress"
echo "Poststress = $poststress"

percentage=$(echo $poststress/$prestress | bc -l)
echo "Load on cpu (relative to normal)" > ~/supermicro_benchmarks/cpu/cpu_test.csv
printf "%.02f" $percentage >> ~/supermicro_benchmarks/cpu/cpu_test.csv
