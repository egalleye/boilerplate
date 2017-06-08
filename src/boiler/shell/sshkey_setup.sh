#!/bin/bash


node_list=("192.168.8.2 192.168.8.3 192.168.8.5")

#ssh node3 'iperf -c 192.168.8.2' | grep sec | awk '{print $7}'

#iperf -s &

for node in $node_list
do
   echo "Node $node"
   #ssh testuser@$node 'echo -e "\n\n\n" | ssh-keygen -t rsa'
   sshpass -p 'xxxxxxxxxx' ssh testuser@$node 'cat ~/.ssh/id_rsa.pub' >> authorized_keys
   sshpass -p 'xxxxxxxxxx' scp authorized_keys_test.txt testuser@$node:~/.ssh/authorized_keys
done

