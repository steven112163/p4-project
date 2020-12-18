# p4-project
Project of Programmable Network Switches Fall 2020 NCTU 可程式化網路交換機 5271  
  
`p4_node.py` is from [p4-tutorial](https://github.com/p4lang/tutorials) and adapted by Steven Yuan (steven112163@gmail.com).



## Virtual Environment  
Pyenv is used because the development environment is Ubuntu 16.04.  
1. Follow instructions in [pyenv-installer](https://github.com/pyenv/pyenv-installer)  

2. Define environment variables for Ubuntu  
    ```shell
    $ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    $ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    ```

3. Add `pyenv init` to the shell  
    ```shell
    $ echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
    ```

4. Restart the shell  
    ```shell
    $ exec "$SHELL"
    ```

5. Install python 3.6.9  
    ```shell
    $ pyenv install 3.6.9
    ```

6. Setup virtual environment for the project  
    ```shell
    $ cd p4-project
    $ pyenv local 3.6.9
    $ pyenv virtualenv <name>
    ```

7. Use the virtual environment for development  
    ```shell
    $ pyenv activate <name>
    ```
    ```shell
    $ pyenv deactivate
    ```



## Prerequisites
* python >= 3.6.9
* scapy >= 2.4.4
* mininet >= 2.3.0.dev6
* psutil >= 5.7.3



## Make
|Command|Description|
|---|---|
|`make build`|Compile p4 program|
|`make clean`|Clean mininet and delete build directory|



## Run  
Python programs are executed on mininet hosts.

### P4 Compilation  
   ```shell
   $ make build
   ```

### Sender  
   ```shell
   $ pyenv activate <name>
   $ python3 sender.py [-src srcIP] [-dst dstIP] [-if interface] [-c count] [-t (0-1)] [-i list_of_ids]
   ```

### Receiver  
   ```shell
   $ pyenv activate <name>
   $ python3 receiver.py [-if interface]
   ```
