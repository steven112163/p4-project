#!/bin/bash

PYENV_ROOT="$HOME/.pyenv"
PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi

PKT_EACH_ROUND=$1
WHETHER_SEND_AGAIN=$2

if [ -n "${PKT_EACH_ROUND}" ]; then
  if [ ${PKT_EACH_ROUND} -lt 1 ]; then
    echo "Packets in each round should be greater or equal to 1."
    exit 1
  fi
fi

if [ -n "${WHETHER_SEND_AGAIN}" ]; then
  if [ ${WHETHER_SEND_AGAIN} -ne 0 ] && [ ${WHETHER_SEND_AGAIN} -ne 1 ]; then
    echo "Argument 'whether_send_again' should be 0 or 1."
    exit 1
  fi
fi

cd host_test || exit
pyenv activate my_p4_environment
iname=$(ls /sys/class/net | grep eth0)

if [ -n "${PKT_EACH_ROUND}" ] && [ -n "${WHETHER_SEND_AGAIN}" ]; then
  python3 sender.py -if "$iname" -c "${PKT_EACH_ROUND}" -ch "${WHETHER_SEND_AGAIN}"
elif [ -n "${PKT_EACH_ROUND}" ]; then
  python3 sender.py -if "$iname" -c "${PKT_EACH_ROUND}"
elif [ -n "${WHETHER_SEND_AGAIN}" ]; then
  python3 sender.py -if "$iname" -ch "${WHETHER_SEND_AGAIN}"
else
  python3 sender.py -if "$iname"
fi