#!/bin/bash
eval "$(pyenv init -)"
cd host_test || exit
pyenv activate my_p4_environment
iname=$(ls /sys/class/net | grep eth0)
if [ -z "$1" ]; then
  python3 sender.py -if "$iname" -c 5
else
  python3 sender.py -if "$iname" -c 5 -ch "$1"
fi