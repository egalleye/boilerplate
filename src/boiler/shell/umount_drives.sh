#!/bin/bash

mnt_dir_base="/mnt/data/"

# EQS NOTE: For nvme's we'll need this line instead of the basic /dev/sd*
lsblk_out=$(lsblk -d | awk '{if(NR>1)print $1}')


for drive_name in ${lsblk_out[@]}
do
    if [ "$drive_name" == "sdn" ]; then
        continue;
    fi
    mnt_dir=$mnt_dir_base$drive_name
    echo "umounting $mnt_dir"
    sudo umount -f $mnt_dir
done 
