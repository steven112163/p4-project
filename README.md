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
|`make aggregate`|Aggregate all random results|



## Python Programs
### sender.py  
Send ARP packets.
```shell
$ python3 sender.py [-src srcIP] [-dst dstIP] [-if interface] [-c count] [-t (0-1)] [-i list_of_ids]
```
|Parameter|Description|Default|
|---|---|---|
|-src, --source|source IP address|'10.0.1.1'|
|-dst, --destination|destination IP address|'10.0.2.2'|
|-if, --interface|name of the interface which sends packets|'h1-eth0'|
|-c, --count|number of packets to be sent|1|
|-t, --test|whether to test variable length field in pure mininet|0 (False)|
|-i, --id|IDs to be placed in variable length field|list(1)|

### receiver.py  
Receive ARP packets and extract the traversed path.  
```shell
$ python3 receiver.py [-if interface]
```  
|Parameter|Description|Default|
|---|---|---|
|-if, --interface|name of the interface on which the sniffer is|'h2-eth0'|

### randomizer.py  
Randomize the link delay between switches.  
```shell
$ python3 randomizer.py [-v (0-1)] [-r (0-1)]
```
|Parameter|Description|Default|
|---|---|---|
|-v, --version|version of the P4 architecture|0 (version 1)|
|-r, --random|randomize or not|0 (False)|

### aggregator.py  
Aggregate all random results.  
```shell
$ python3 aggregator.py [-d name_of_the_directory] [-c num_of_packets]
```  
|Parameter|Description|Default|
|---|---|---|
|-d, --directory|name of the directory|'results'|
|-c, --count|number of packets sent in each round|5|



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
