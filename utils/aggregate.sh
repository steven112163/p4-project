#!/bin/bash

PKT_EACH_ROUND=$1

if [ -z "${PKT_EACH_ROUND}" ]; then
  echo "Usage: $0 <number of packets in each round>."
  exit 1
fi

if [ ${PKT_EACH_ROUND} -lt 1 ]; then
  echo "Number of packets in each round should be greater or equal to 1."
  exit 1
fi

eval "$(pyenv init -)"
pyenv activate my_p4_environment
sudo chmod -R 777 results
python3 utils/aggregator.py -c ${PKT_EACH_ROUND}