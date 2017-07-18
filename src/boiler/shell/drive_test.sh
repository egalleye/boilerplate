#!/bin/bash

os_drive="sdn"
username="test"
one="1"
mnt_dir_base="/mnt/data/"
bigddfile="bigddfile.out"
outputdir="/home/$username/supermicro_benchmarks/drive/"
ext=".txt"
dev_dir="/dev/"
fio_runtime=240
fiopids=""
fiostr="_fio.out"
smrtctlstr="_smartctl.out"
ddstr="_dd.out"
hdparmstr="_hdparm.out"
drivetime=0

#### Disc test setup ####

# Get list of all available drives
drive_list=$(lsblk -d | awk '{if(NR>1)print $1}')

# Initialize directories  
sudo mkdir -p /mnt/data
sudo chown -R $username:$username /mnt/data



get_drivetest_timetorun() {
    drivetime=$(cat supermicro_benchmark.config | grep "drivetime" | sed -e 's/=/ /g' | awk '{print $2}')
    
    timeunits=$(echo "${drivetime: -1}")
    TIMEOUT=${drivetime::-1}
    
    if [ "$timeunits" == 'S' ] || [ "$timeunits" == 's' ]
    then
        timeunitsstr="seconds"
        timeseconds=$TIMEOUT
        echo "sTimeout = $TIMEOUT"
    elif [ "$timeunits" == 'M' ] || [ "$timeunits" == 'm' ]
    then
        timeunitsstr="minutes"
        timeseconds=$(echo "$TIMEOUT * 60" | bc -l)
        echo "mTimeout = $TIMEOUT"
    elif [ "$timeunits" == 'H' ] || [ "$timeunits" == 'h' ]
    then
        timeunitsstr="hours"
        timeseconds=$(echo "$TIMEOUT * 3600" | bc -l)
        echo "hTimeout = $TIMEOUT"
    else
        echo "No time"
        timeseconds=$TIMEOUT
    fi
    
    echo "Running drive test for $timeseconds seconds"
}

partition_drives() {
    # Partition each drive
    for drive_name in ${drive_list[@]}
    do
        drive="$dev_dir$drive_name"
        # EQS NOTE: Take this out for real test
        if [ "$drive_name" == $os_drive ]; then
            continue;
        fi
        sudo parted -s -a optimal $drive mklabel gpt -- mkpart primary ext4 1 -1 &
    done
    
    while [ 1 ]
    do
        parted_running=$(pgrep "parted")
        if [ -z "$mkfs_running" ] 
        then
            echo "parted finished!"
            break
        else
            echo "parted Running"
            sleep 8
        fi
    done

}

mkfs_drives() {
    # Write filesystem to each drive, create dirs for each
    for drive_name in ${drive_list[@]}
    do
        drive="$dev_dir$drive_name"
        sudo mkfs.ext4 -q $drive$one &
        if [ "$drive_name" == $os_drive ]; then
            continue;
        fi
    
        sudo mkdir $mnt_dir_base$drive_name
    done 

    while [ 1 ]
    do
        mkfs_running=$(pgrep "mkfs")
        if [ -z "$mkfs_running" ] 
        then
            echo "mkfs finished!"
            break
        else
            echo "mkfs Running"
            sleep 2
        fi
    done

}


mount_drives() {
    # Mount drives
    for drive_name in ${drive_list[@]}
    do
        drive="$dev_dir$drive_name"
        if [ "$drive_name" == $os_drive ]; then
            continue;
        fi
        mnt_dir=$mnt_dir_base$drive_name
        sudo mount $drive$one $mnt_dir
        sudo chown -R $username:$username $mnt_dir
    done 


}

get_temperature_drives() {
    for drive_name in ${drive_list[@]}
    do
        drive="$dev_dir$drive_name"
        smrtctl_outfile="/tmp/$drive_name$smrtctlstr"
        echo "Smartctl outfile = $smrtctl_outfile"
        # Enable smartctl
        sudo smartctl -q errorsonly -s on $drive
        #sudo smartctl -t long $drive
        # Get drivetype '0' for SSD, '1' for HDD
        drivetype=$(cat /sys/block/$drive_name/queue/rotational)
        if [ $drivetype -eq 0 ]; then
            # SSDs
            sudo smartctl -a $drive | grep "Temperature_Celsius" | awk '{print $10}' > $smrtctl_outfile
        else
            # HDDs
            sudo smartctl -a $drive | grep "Drive Temp" | awk '{print $4}' > $smrtctl_outfile

        fi
    done
}


run_fio() {

    ## FIO Test ##
    for drive_name in ${drive_list[@]}
    do
        if [ "$drive_name" == "sdn" ]; then
            continue;
        fi
    
        drive="$dev_dir$drive_name"
        mnt_dir=$mnt_dir_base$drive_name
        echo "Drive $mnt_dir/benchtest"
        fio_outfile="/tmp/$drive_name$fiostr"
    
        fio_out=$(fio --name=random-writers --ioengine=libaio --iodepth=16 --rw=randwrite --bs=32k --direct=0 --size=64m --time_based --runtime=$fio_runtime --filename=$mnt_dir/benchtest > $fio_outfile &)
    done

    while [ 1 ]
    do
        fio_running=$(pgrep "fio")
        if [ -z "$fio_running" ] 
        then
            echo "fio finished!"
            break
        else
            echo "fio Running"
            sleep 2
        fi
    done
}

run_hdparm() {

    for drive_name in ${drive_list[@]}
    do
        drive="$dev_dir$drive_name"
        mnt_dir=$mnt_dir_base$drive_name
        hdparm_outfile="/tmp/$drive_name$hdparmstr"
        hdparm_out=$(sudo hdparm -tT $drive | grep "disk reads:" | awk '{print $11}' > $hdparm_outfile &)
    done 
    
    while [ 1 ]
    do
        hdparm_running=$(pgrep "hdparm")
        if [ -z "$hdparm_running" ] 
        then
            echo "hdparm finished!"
            break
        else
            echo "hdparm Running"
            sleep 2
        fi
    done


}

clean_drives() {
    for drive_name in ${drive_list[@]}
    do
    
        if [ "$drive_name" == "sdn" ]; then
            continue;
        fi
        ## Clean up ##
        mnt_dir=$mnt_dir_base$drive_name
    
        echo "umounting $mnt_dir"
        sudo umount -f $mnt_dir
        # Remove Partition 
        sudo parted -s $drive rm 1
    done
    
    for drive_name in ${drive_list[@]}
    do
        ## dd test (zeros) ##
        dd_outfile="/tmp/$drive_name$ddstr"
        ddspeed=$(sudo dd if=/dev/zero of=$mnt_dir$bigddfile bs=64M count=1 iflag=fullblock |& grep "bytes" | awk '{print $8 $9}' | sed -e 's/\//p/g' &)
        #ddfourg_speed=$(sudo dd if=/dev/zero of=$mnt_dir$bigddfile bs=64M count=64 iflag=fullblock |& grep "bytes" | awk '{print $8 $9}' | sed -e 's/\//p/g')
    
        echo "dd speed $ddspeed" > $dd_outfile
    done
}

consolidate_stats() {
    for drive_name in ${drive_list[@]}
    do
        if [ "$drive_name" == "sdn" ]; then
            continue;
        fi
        drive="$dev_dir$drive_name"
        mnt_dir=$mnt_dir_base$drive_name
        fio_outfile="/tmp/$drive_name$fiostr"
        hdparm_outfile="/tmp/$drive_name$hdparmstr"
        dd_outfile="/tmp/$drive_name$ddstr"
        smrtctl_outfile="/tmp/$drive_name$smrtctlstr"
    
        hdparm=$(cat $hdparm_outfile)
        dd_out=$(cat $dd_outfile)
    
        drive_bandwidth=$(cat $fio_outfile | grep "write" | grep "bw" | awk '{print $3}' | sed -e 's/[^0-9.]*//g')
        drive_clat=$(cat $fio_outfile | grep "stdev" | grep "clat" | awk '{print $5}' | sed -e 's/[^0-9.]*//g')
        smrtctl_temp_c=$(cat $smrtctl_outfile)
        
        echo "fio_bandwidth_kbps, fio_clat_avg_usec, hdparm_mbps, dd_64mb, drive_temp_celsius" > $outputdir$drive_name$ext
        echo "$drive_bandwidth, $drive_clat, $hdparm, $dd_out, $smrtctl_temp_c" >> $outputdir$drive_name$ext
        echo "fio bandwidth is $drive_bandwidth"
        echo "fio clat is $drive_clat"
        echo "hdparm is $hdparm"
        echo "dd out is $dd_out"
        echo "Drive temperature is $smrtctl_temp_c"
    done
}

main() {
    get_drivetest_timetorun
    partition_drives
    mkfs_drives
    mount_drives
    get_temperature_drives
    run_fio
    run_hdparm
    clean_drives
    consolidate_stats
}
main
