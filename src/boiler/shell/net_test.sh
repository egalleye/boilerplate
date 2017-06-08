#!/bin/bash


node_list=("192.168.8.2 192.168.8.3 192.168.8.5")

iperf -s &
iperfcsv=""
csvheader=""
iter=0

host=$(hostname -I)
echo "Host is $host"

for node in $node_list
do
   echo "Running iperf from node $node"
   iperf_cli_out=$(ssh test@$node "iperf -c $host")

   iperf_out=$(echo "$iperf_cli_out" | grep sec | awk '{print $7}') 

   if [ "$iter" -eq "0" ]
   then
       echo "iter is zero $iter"
       csvheader="$node"
       iperfcsv="$iperf_out"
   else
       csvheader="$csvheader, $node"
       iperfcsv="$iperfcsv, $iperf_out"
   fi
   

   ((iter++))
done

echo "$csvheader" > ~/supermicro_benchmarks/net/net_test.txt
echo "$iperfcsv" >> ~/supermicro_benchmarks/net/net_test.txt


# Cleanup
sudo pkill iperf
