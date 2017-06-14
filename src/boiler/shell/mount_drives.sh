#!/bin/bash


one="1"
mnt_dir_base="/mnt/data/"
bigddfile="bigddfile.out"
outputdir="/home/test/supermicro_benchmarks/drive/"
ext=".txt"
dev_dir="/dev/"

# EQS NOTE: For nvme's we'll need this line instead of the basic /dev/sd*
lsblk_out=$(lsblk -d | awk '{if(NR>1)print $1}')

#### Disc test ####

## FIO setup ##
sudo mkdir -p /mnt/data
sudo chown -R test:test /mnt/data

# Partition each drive
for drive_name in ${lsblk_out[@]}
do
    drive="$dev_dir$drive_name"
    # EQS NOTE: Take this out for real test
    if [ "$drive_name" == "sdn" ]; then
        continue;
    fi
    sudo parted -s -a optimal $drive mklabel gpt -- mkpart primary ext4 1 -1 &
done

wait

# Write filesystem to each drive, create dirs for each
for drive_name in ${lsblk_out[@]}
do
    drive="$dev_dir$drive_name"
    sudo mkfs.ext4 $drive$one &
    if [ "$drive_name" == "sdn" ]; then
        continue;
    fi

    sudo mkdir $mnt_dir_base$drive_name
done 

wait

# Mount drives
for drive_name in ${lsblk_out[@]}
do
    drive="$dev_dir$drive_name"
    if [ "$drive_name" == "sdn" ]; then
        continue;
    fi
    mnt_dir=$mnt_dir_base$drive_name
    sudo mount $drive$one $mnt_dir
    sudo chown -R test:test $mnt_dir
done 


