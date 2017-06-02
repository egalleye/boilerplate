#!/bin/bash

stress -c 2 -i 1 -m 1 --vm-bytes 1024M -t 10s
