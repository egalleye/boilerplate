#!/bin/bash

one="1"
mnt_dir="/mnt/data/"
output_dir="/hdwr_test/drives/"
bigddfile="bigddfile.out"
tmpfile="tmp.out"
fileext=".txt"

declare -a drives=("/dev/sda"
                "/dev/sdb"
                "/dev/sdc"
                "/dev/sdd"
                "/dev/sde"
                "/dev/sdf"
                "/dev/sdg"
                "/dev/sdh"
                "/dev/sdi"
                "/dev/sdj"
                "/dev/sdk"
                "/dev/sdl"
                "/dev/sdm"
                )


for drive in "${drives[@]}"
do
    sudo mount $drive$one $mnt_dir
    drive_name=$(echo "$drive" | sed -e 's/\/dev\///g')

#    echo "$drive_name's dd speed:"

    ddspeed=$(sudo dd if=/dev/zero of=$mnt_dir$bigddfile bs=64M count=1 iflag=fullblock |& grep "bytes" | awk '{print $8 $9}' | sed -e 's/\//p/g')

#    echo "$ddspeed"
    echo "dd_64Mb" > "/home/test/scratch/$tmpfile" 
    echo "$ddspeed" >> "/home/test/scratch/$tmpfile" 

    ddrandspeed=$(sudo dd if=/dev/zero of=$mnt_dir$bigddfile bs=64M count=64 iflag=fullblock |& grep "bytes" | awk '{print $8 $9}' | sed -e 's/\//p/g')
    sed_line="sed -e '2s/$/, $ddrandspeed/'"
    cat "$tmpfile" | sed '1s/$/, dd_4Gb/' | eval $sed_line | tee "$output_dir$drive_name$fileext"
    sudo rm -f "$mnt_dir/*"
    sudo umount -f $mnt_dir
    #echo "$drive"
done

