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

## FIO Test ##
for drive_name in ${lsblk_out[@]}
do
    if [ "$drive_name" == "sdn" ]; then
        continue;
    fi
    echo "################ FIO ################"

    drive="$dev_dir$drive_name"
    mnt_dir=$mnt_dir_base$drive_name
    echo "Drive $mnt_dir/benchtest"

    fio_out=$(fio --name=random-writers --ioengine=libaio --iodepth=16 --rw=randwrite --bs=32k --direct=0 --size=64m --time_based --runtime=24 --filename=$mnt_dir/benchtest > /tmp/$drive_name &)

    #echo "################ Cleanup ################"
    ## Clean up ##
    #sudo rm -f "$mnt_dir/*"
    #sudo umount -f $mnt_dir
    # Remove Partition 
    #sudo parted -s $drive rm 1

    ## dd test (zeros) ##
    #echo "################ dd tests ################"
    #ddspeed=$(sudo dd if=/dev/zero of=$mnt_dir$bigddfile bs=64M count=1 iflag=fullblock |& grep "bytes" | awk '{print $8 $9}' | sed -e 's/\//p/g')
    #ddfourg_speed=$(sudo dd if=/dev/zero of=$mnt_dir$bigddfile bs=64M count=64 iflag=fullblock |& grep "bytes" | awk '{print $8 $9}' | sed -e 's/\//p/g')

    #echo "fio_bandwidth_kbps, fio_clat_usec, dd_64M_speed, dd_4G_speed" > $outputdir$drive_name$ext
    #echo "$drive_bandwidth, $drive_clat, $ddspeed, $ddfourg_speed" >> $outputdir$drive_name$ext

done


wait
sleep 25

for drive_name in ${lsblk_out[@]}
do
    if [ "$drive_name" == "sdn" ]; then
        continue;
    fi
    drive="$dev_dir$drive_name"
    mnt_dir=$mnt_dir_base$drive_name

    drive_bandwidth=$(cat /tmp/$drive_name | grep "write" | grep "bw" | awk '{print $3}' | sed -e 's/[^0-9.]*//g')
    drive_clat=$(cat /tmp/$drive_name | grep "stdev" | grep "clat" | awk '{print $5}' | sed -e 's/[^0-9.]*//g')
    echo "fio_bandwidth_kbps, fio_clat_used" > $outputdir$drive_name$ext
    echo "$drive_bandwidth, $drive_clat" >> $outputdir$drive_name$ext
    echo "fio bandwidth is $drive_bandwidth"
    echo "fio clat is $drive_clat"
done


for drive_name in ${lsblk_out[@]}
do
    if [ "$drive_name" == "sdn" ]; then
        continue;
    fi
    mnt_dir=$mnt_dir_base$drive_name
    echo "umounting $mnt_dir"
    sudo umount -f $mnt_dir
done 

