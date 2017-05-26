#!/bin/bash


declare -a drives=("/dev/drivename1"
                "/dev/drivename2"
                "/dev/drivename3"
                )


for drive in "${drives[@]}"
do
    sudo parted -s -a optimal $drive mklabel gpt -- mkpart primary ext4 1 -1
    sudo mkfs.ext4 $drive
    #echo "$drive"
done

