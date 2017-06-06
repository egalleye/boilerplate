#!/bin/bash

num_cpus=8
echo "cpu_stress" > /hdwr_test/cpu/cpu_test.txt
stress -c $num_cpus -i 1 -m 1 --vm-bytes 1024M -t 32s
uptime | awk '{print $8}' | sed 's/[^0-9.]*//g' >> /hdwr_test/cpu/cpu_test.txt
