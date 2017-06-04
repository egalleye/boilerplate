#!/bin/bash



mem_total_str=$(free -h | grep "Mem:" | awk '{print $2}')
mem_used_str=$(free -h | grep "Mem:" | awk '{print $3}')

mt_units="${mem_total_str: -1}"
mu_units="${mem_used_str: -1}"

# EQS NOTE: This needs to be fleshed out into an 
#           actual conversion
# Write in guard against having different units
if [ "$mt_units" != "$mu_units" ];then
    exit -1;
fi

mem_total=$(echo "$mem_total_str" |  sed -e 's/[^0-9]*//g')
mem_used=$(echo "$mem_used_str" | sed -e 's/[^0-9]*//g')

#mem_percent_used=$(bc <<<"scale=2 $mem_used / $mem_total")
mem_decimal_used=$(echo "$mem_used / $mem_total" | bc -l)
mem_percent_used=$(echo "$mem_decimal_used * 100" | bc -l)

printf "%0.2f\n" $mem_percent_used

