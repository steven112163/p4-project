#!/bin/bash
PYENV_ROOT="$HOME/.pyenv"
PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi
cd host_test || exit
pyenv activate my_p4_environment
iname=$(ls /sys/class/net | grep eth0)
python3 receiver.py -if "$iname"