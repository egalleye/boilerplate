#!/bin/bash

DISK="/dev/sda/"

# Sed line filters out all chars that are not digit or '.'
disc_total_capacity=$(df -h | grep /dev/sda | awk '{print $2}' | sed 's/[^0-9\.]*//g')
disc_space_used=$(df -h | grep /dev/sda | awk '{print $3}' | sed 's/[^0-9\.]*//g')
disc_use_percent=$(df -h | grep /dev/sda | awk '{print $5}' | sed 's/[^0-9\.]*//g')
echo "Disk capacity,    Disk space used,  Percent of disk space used" > disc_usage.out
echo "$disc_total_capacity,  $disc_space_used,    $disc_use_percent" >> disc_usage.out

