#!/bin/bash

one="1"
mnt_dir="/mnt/data/"
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
    echo "dd_speed" > "/home/test/scratch/$tmpfile" 
    echo "$ddspeed" >> "/home/test/scratch/$tmpfile" 

    ddrandspeed=$(sudo dd if=/dev/zero of=$mnt_dir$bigddfile bs=64M count=10 iflag=fullblock |& grep "bytes" | awk '{print $8 $9}' | sed -e 's/\//p/g')
    sed_line="sed -e '2s/$/, $ddrandspeed/'"
    cat "$tmpfile" | sed '1s/$/, dd_res2/' | eval $sed_line | tee "$drive_name$fileext"
    cat "$tmpfile" | eval $sed_line 
    sudo umount -f $mnt_dir
    #echo "$drive"
done

