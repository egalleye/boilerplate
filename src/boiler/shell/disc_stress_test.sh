#!/bin/bash

# NOTE: CAREFUL! THIS WILL WRITE A 16G file!
sudo dd if=/dev/urandom of=bigfile.out bs=64M count=256 iflag=fullblock
