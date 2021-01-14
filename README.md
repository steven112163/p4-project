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
* tmux
* [p4-utils](https://github.com/nsg-ethz/p4-utils)



## Make
|Command|Description|
|---|---|
|`make build`|Compile p4 program|
|`make clean`|Clean mininet and delete environment-related directory|
|`make clean_all`|`make clean` and delete results|
|`make aggregate`|Aggregate all random results|  

### Version 1  
|Command|Description|
|---|---|
|`make run1`|Start version 1 test|
|`make worst1`|Start version 1 worst case test|
|`make random1`|Start version 1 test with random link delay|
|`make ten1`|Start version 1 test with random link delay and 10 switches|
|`make tf1`|Start version 1 test with random link delay and 25 switches|
|`make fif1`|Start version 1 test with random link delay and 50 switches|

### Version 2  
|Command|Description|
|---|---|
|`make run2`|Start version 2 test|
|`make worst2`|Start version 2 worst case test|
|`make random2`|Start version 2 test with random link delay|
|`make ten2`|Start version 2 test with random link delay and 10 switches|
|`make tf2`|Start version 2 test with random link delay and 25 switches|
|`make fif2`|Start version 2 test with random link delay and 50 switches|



## Python Programs
### sender.py  
Send ARP packets.
```shell
$ python3 sender.py [-src srcIP] [-dst dstIP] [-if interface] [-c count] [-ch (0-1)] [-t (0-1)] [-i list_of_ids]
```
|Parameter|Description|Default|
|---|---|---|
|-src, --source|Source IP address|'10.0.1.1'|
|-dst, --destination|Destination IP address|'10.0.2.2'|
|-if, --interface|Name of the interface which sends packets|'h1-eth0'|
|-c, --count|Number of packets to be sent|1|
|-ch, --check|Whether send packets again to test convergence|0|
|-t, --test|Whether to test variable length field in pure mininet|0 (False)|
|-i, --id|IDs to be placed in variable length field|list(1)|

### receiver.py  
Receive ARP packets and extract the traversed path.  
```shell
$ python3 receiver.py [-if interface]
```  
|Parameter|Description|Default|
|---|---|---|
|-if, --interface|Name of the interface on which the sniffer is|'h2-eth0'|

### randomizer.py  
Randomize the link delay between switches.  
```shell
$ python3 randomizer.py [-v (0-1)] [-r (0-2)] [-n (>= 3)]
```
|Parameter|Description|Default|others|
|---|---|---|---|
|-v, --version|Version of the P4 architecture|0 (version 1)|1 (version 2)|
|-r, --random|Mode of link delay|0 (equal link delay)|1 (worst Case), 2 (random link delay)|
|-n, --number|Number of switches|3||

### aggregator.py  
Aggregate all random results.  
```shell
$ python3 aggregator.py [-d name_of_the_directory] [-c num_of_packets] [-r num_of_rounds]
```  
|Parameter|Description|Default|
|---|---|---|
|-d, --directory|Name of the directory|'results'|
|-c, --count|Number of packets sent in each round|5|
|-r, --round|Number of rounds in each test|2|



## Run  
Python programs are executed on mininet hosts.

### Auto Test  
1. Start testing.
   ```shell
   $ make run1
   or
   $ make worst1
   or
   $ make random1
   or
   $ make ten1
   or
   $ make tf1
   or
   $ make fif2
   ```  
   or
   ```shell
   $ make run2
   or
   $ make worst2
   or
   $ make random2
   or
   $ make ten2
   or
   $ make tf2
   or
   $ make fif2
   ```

2. Show results.
   ```shell
   $ make aggregate
   ```

### Manual Test
1. Setup required files for the environment.  
   ```shell
   $ python3 randomizer.py [-v (0-1)] [-r (0-2)] [-n (>= 3)]
   ```

2. Start the environment.
   ```shell
   $ sudo p4run
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
   $ sh send.sh [0 or 1]
   ```

6. Execute the aggregator in another terminal to see the result.
   ```shell
   $ python3 aggregator.py [-d name_of_the_directory] [-c num_of_packets] [-r num_of_rounds]
   ```

### Sender  
   ```shell
   $ pyenv activate my_p4_environment
   $ cd host_test
   $ python3 sender.py [-src srcIP] [-dst dstIP] [-if interface] [-c count] [-ch (0-1)] [-t (0-1)] [-i list_of_ids]
   ```

### Receiver  
   ```shell
   $ pyenv activate my_p4_environment
   $ cd host_test
   $ python3 receiver.py [-if interface]
   ```
