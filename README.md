# p4-project
Project of Programmable Network Switches Fall 2020 NCTU 可程式化網路交換機 5271



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
    $ pyenv virtualenv my_p4_environment
    ```

7. Use the virtual environment for development  
    ```shell
    $ pyenv activate my_p4_environment
    ```
    ```shell
    $ pyenv deactivate
    ```



## Prerequisites
* python >= 3.6.9
* scapy >= 2.4.4
* mininet >= 2.3.0.dev6
* pandas >= 1.1.5
* matplotlib >= 3.3.3
* [p4-utils](https://github.com/nsg-ethz/p4-utils)



## Make
|Command|Description|
|---|---|
|`make build`|Compile p4 program|
|`make clean`|Clean mininet and delete environment-related directory|
|`make clean_all`|`make clean` and delete results|
|`make run1`|Start version 1 test|
|`make run_random1`|Start version 1 test with random link delay|
|`make run2`|Start version 2 test|
|`make run_random2`|Start version 2 test with random link delay|



## Run  
Python programs are executed on mininet hosts.

1. Rewrite `p4app.json.txt` to set up current test environment.

2. Start test environment.  
   ```shell
   $ make run1
   ```  
   or  
   ```shell
   $ make run_random1
   ```  
   or  
   ```shell
   $ make run2
   ```  
   or  
   ```shell
   $ make run_random2
   ```

3. Call the terminals of sender and receiver.
   ```shell
   $ xterm h1 h2
   ```

4. Start receiver in h2.
   ```shell
   $ sh receive.sh
   ```

5. Start sender in h1.
   ```shell
   $ sh send.sh
   ```

6. Terminate the process in h2 with `ctrl+c` to see the result graph.

### Sender  
   ```shell
   $ pyenv activate my_p4_environment
   $ cd host_test
   $ python3 sender.py [-src srcIP] [-dst dstIP] [-if interface] [-c count] [-t (0-1)] [-i list_of_ids]
   ```

### Receiver  
   ```shell
   $ pyenv activate my_p4_environment
   $ cd host_test
   $ python3 receiver.py [-if interface]
   ```
