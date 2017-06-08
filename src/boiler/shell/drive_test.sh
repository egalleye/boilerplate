#!/bin/bash


one="1"
mnt_dir="/mnt/data/"
bigddfile="bigddfile.out"
outputdir="/home/test/supermicro_benchmarks/drive/"
ext=".txt"

# EQS NOTE: For nvme's we'll need this line instead of the basic /dev/sd*
#ls_out=$(ls /dev/sd*; ls /dev/nvme*)
ls_out=$(ls /dev/sd*)

#### Disc test ####

## FIO setup ##
sudo mkdir -p /mnt/data
sudo chown -R test:test /mnt/data

for drive in ${ls_out[@]}
do
    
    while [ 1 ] 
    do
        if ! df -h | grep -q '$mnt_dir'; then
        	break;
        else
        	echo "$drive still mounted"
                sudo umount -f $mnt_dir
        	sleep 1
        fi
    done
    drive_name=$(echo "$drive" | sed -e 's/\/dev\///g')
    # EQS NOTE: Take this out for real test
    if [ "$drive_name" == "sdn" ]; then
        exit 0;
    fi
    echo "$drive_name"
    sudo parted -s -a optimal $drive mklabel gpt -- mkpart primary ext4 1 -1
    sudo mkfs.ext4 $drive$one

    sudo mount $drive$one $mnt_dir
    sudo chown -R test:test $mnt_dir
    ## FIO Test ##
    echo "################ FIO ################"
    fio_out=$(fio random_read_test.fio)
    drive_bandwidth=$(echo "$fio_out" | grep "stdev" | grep "bw" | awk '{print $10}' | sed -e 's/stdev=//g')
    drive_clat=$(echo "$fio_out" | grep "stdev" | grep "clat" | awk '{print $6}' | sed -e 's/stdev=//g')

    echo "################ Cleanup ################"
    ## Clean up ##
    sudo rm -f "$mnt_dir/*"
    sudo umount -f $mnt_dir
    # Remove Partition 
    sudo parted -s $drive rm 1

    ## dd test (zeros) ##
    echo "################ dd tests ################"
    ddspeed=$(sudo dd if=/dev/zero of=$mnt_dir$bigddfile bs=64M count=1 iflag=fullblock |& grep "bytes" | awk '{print $8 $9}' | sed -e 's/\//p/g')
    ddfourg_speed=$(sudo dd if=/dev/zero of=$mnt_dir$bigddfile bs=64M count=64 iflag=fullblock |& grep "bytes" | awk '{print $8 $9}' | sed -e 's/\//p/g')

    echo "fio_bandwidth_kbps, fio_clat_usec, dd_64M_speed, dd_4G_speed" > $outputdir$drive_name$ext
    echo "$drive_bandwidth, $drive_clat, $ddspeed, $ddfourg_speed" >> $outputdir$drive_name$ext

done
