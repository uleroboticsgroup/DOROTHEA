# DOROTHEA

<big>**Do**cker-based f**r**amework f**o**r ga**th**ering n**e**tflow tr**a**ffic</big>

![GitHub Release](https://img.shields.io/github/v/release/uleroboticsgroup/DOROTHEA)
![GitHub License](https://img.shields.io/github/license/uleroboticsgroup/DOROTHEA)


## Description
The primary objective of this framework is to establish an environment that comprehensively monitors and captures all network flows. This is accomplished through the creation of a virtual network and use of Docker containers to run a NetFlow exporter `softflowd` and a collector `nfcaps` to handle the flows.

All interactions within this virtual LAN are captured, parsed, and subsequently exported as IPFIX NetFlows. These NetFlows are stored as nfcaps and are additionally converted into a more user-friendly CSV format, facilitating easier analysis and interpretation.

Moreover, the framework includes various tools designed to simplify the execution of commands and scripts on its predefined worker nodes.

### Key Objectives

- **Realistic Netflow Generation:** The framework's primary objective is to generate netflows that closely resemble real network traffic. These netflows simulate genuine interactions and transactions, creating a robust dataset for training machine learning models.

- **Malicious Activity Training Data:** The generated netflows are intended for use as training data in the development of models specialized in identifying malicious network activity. This enables the enhancement of security mechanisms and the proactive detection of potential threats.

- **Virtual Network Environment:** By establishing a virtual LAN and deploying containerized nodes, the framework creates a controlled network environment that mimics real-world networking scenarios. This environment facilitates the generation and monitoring of traffic patterns while maintaining a low profile in resource consumption.

- **Effective Monitoring with `softflowd` and `nfcap`:** The framework employs `softflowd` as a netflow exporter and `nfcap` as a netflow collector, enabling comprehensive monitoring of all interactions within the virtual network. This monitoring captures and parses traffic data, exporting it as netflows.




## Requirements
*   Docker Engine
*   Python3

## Usage

>  In case of using Windows, execute from WSL to avoid unknown bugs.

In order to run the framework, first edit the file `actions_list.yml` and add the scripts you would like to run under `containers/<container_type>/user_actions_scripts`. Then simply run the script and wait for flow generation.


```bash
$ cd DOROTHEA
$ pip3 install -r requirements.txt
$ python3 dorothea
```
### Tips

While running, you can access the Rabbit-MQ manager to see the status of the queues at:

[http://localhost:15672](http://localhost:15672)

**user**: `dorothea`  **pass**: `dorothea`


To see the execution/consumption of each node, just print its logs:
```bash
$ docker logs <dorothea_node>
```

## Configuration

In order to add more user interactions to the framework, add new entries under one of both YAML configuration files:
- `vanilla_actions.yml`
- `hostile_actions.yml` 

If the actions use a script, move them to the corresponding folder `containers/<container_type>/user_actions_scripts`. Required dependencies for the script will be added to the `Dockerfile` and to the `requirements.txt` under the same directory.

In addition to the already preconfigured containers, you can run additional ones to be monitored for netflows by attaching them to the `lan_dorothea` Docker network when **Dorothea** is running.


## Repository structure

In the root directory of this repo, you can find:


* `dorothea` directory containing the DOROTHEA Python code.

* The files `vanilla_actions.yml` and `hostile_actions.yml`, which are lists of the actions to execute in the nodes.

* The directory `containers` contains one subdirectory for each Docker image to be built, with resources needed to build it.

* And after running the script, a directory named `dump` should appear containing the outputs of the script.

## License
This framework is released under the [LGPL-3.0](LICENSE). Feel free to use, modify, and distribute it in accordance with the terms of the license.

