#!/bin/bash
eval "$(pyenv init -)"
cd host_test || exit
pyenv activate my_p4_environment
iname=$(ls /sys/class/net | grep eth0)
python3 receiver.py -if "$iname"