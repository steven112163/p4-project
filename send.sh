#!/bin/bash
eval "$(pyenv init -)"
cd host_test || exit
pyenv activate my_p4_environment
python3 sender.py -c 5