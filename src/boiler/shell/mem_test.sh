#!/bin/bash

TIMEOUT=60

memtime=$(cat supermicro_benchmark.config | grep "memorytime" | sed -e 's/=/ /g' | awk '{print $2}')

echo "memtime is $memtime"

timeunits=$(echo "${memtime: -1}")
TIMEOUT=${memtime::-1}

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

echo "Running MEM test for $timeseconds seconds"

echo "stressapptest" > ~/supermicro_benchmarks/mem/mem_test.txt
stressapptest -s $timeseconds -M 32768 -m 8 -W | grep "Memory" | awk '{print $6}' >> ~/supermicro_benchmarks/mem/mem_test.txt
