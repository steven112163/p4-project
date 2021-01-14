#!/bin/bash

SESSION="P4ProjectTest"

NUM_OF_HOSTS=$1
NUM_OF_TESTS=$2
P4_ARCHI_VERSION=$3
RANDOM_VERSION=$4

if [ -z "${NUM_OF_HOSTS}" ] || [ -z "${NUM_OF_TESTS}" ] || [ -z "${P4_ARCHI_VERSION}" ] || [ -z "${RANDOM_VERSION}" ]; then
  echo "Usage: $0 <number of hosts> <number of tests> <version of P4 architecture> <random version>."
  exit 1
fi

if [ ${NUM_OF_HOSTS} -lt 3 ]; then
  echo "Number of hosts should be greater or equal to 3."
  exit 1
fi

if [ ${NUM_OF_TESTS} -lt 1 ]; then
  echo "Number of tests should be greater than 1."
  exit 1
fi

if [ ${P4_ARCHI_VERSION} -ne 0 ] && [ ${P4_ARCHI_VERSION} -ne 1 ]; then
  echo "Version of P4 architecture should be 0 or 1."
  exit 1
fi

if [ ${RANDOM_VERSION} -ne 0 ] && [ ${RANDOM_VERSION} -ne 1 ] && [ ${RANDOM_VERSION} -ne 2 ]; then
  echo "Random version should be 0, 1 or 2."
  exit 1
fi

sudo tmux start-server

if [ "$(sudo tmux ls | grep ${SESSION})" ]; then
  sudo tmux kill-session -t ${SESSION}
fi

sudo tmux new-session -d -s ${SESSION} -n p4_project
sudo tmux set remain-on-exit on

for test_no in $(seq 1 ${NUM_OF_TESTS}); do
  echo "** Test ${test_no}"

  sudo tmux send-keys -t 1 "python3 utils/randomizer.py -v ${P4_ARCHI_VERSION} -r ${RANDOM_VERSION} -n ${NUM_OF_HOSTS}" Enter
  sleep 0.5s

  echo "** Starting environment ..."
  sudo tmux send-keys -t 1 "p4run" Enter
  if [ ${NUM_OF_HOSTS} -ge 25 ]; then
    sleep 1m 20s
  elif [ ${NUM_OF_HOSTS} -ge 10 ]; then
    sleep 20s
  else
    sleep 10s
  fi

  for host_id in $(seq 2 ${NUM_OF_HOSTS}); do
    echo "*** h${host_id} starts receiving"
    sudo tmux send-keys -t 1 "noecho h${host_id} make receive" Enter
    sleep 5s
  done

  sudo tmux send-keys -t 1 "noecho h1 make send" Enter
  echo "*** h1 starts sending"
  sleep 5s

  sudo tmux send-keys -t 1 "exit" Enter
  echo "** Shutdown environment ..."
  if [ ${NUM_OF_HOSTS} -ge 25 ]; then
    sleep 50s
  elif [ ${NUM_OF_HOSTS} -ge 10 ]; then
    sleep 10s
  else
    sleep 5s
  fi

  sudo tmux send-keys -t 1 "make clean" Enter
  echo "** Cleaning ..."
  sleep 5s
done

echo "** Finished"
sudo tmux kill-session -t ${SESSION}
