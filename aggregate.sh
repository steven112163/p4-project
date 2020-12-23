#!/bin/bash
eval "$(pyenv init -)"
pyenv activate my_p4_environment
sudo chmod -R 777 results
python3 aggregator.py