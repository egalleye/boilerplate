#!/bin/bash

echo "SAT" > /hdwr_test/mem/mem_test.txt
stressapptest -s 20 -M 256 -m 4 -W | grep "Memory" | awk '{print $6}' >> /hdwr_test/mem/mem_test.txt
