#!/bin/bash

# Add user test
sudo bash -c "echo \"testuser    ALL=(ALL:ALL) NOPASSWD:ALL\" >> /etc/sudoers"
