# DOROTHEA

[![Dorothea CI](https://github.com/uleroboticsgroup/DOROTHEA/actions/workflows/dorothea.yml/badge.svg)](https://github.com/uleroboticsgroup/DOROTHEA/actions/workflows/dorothea.yml)
[![Examples CI](https://github.com/uleroboticsgroup/DOROTHEA/actions/workflows/examples.yml/badge.svg)](https://github.com/uleroboticsgroup/DOROTHEA/actions/workflows/examples.yml)

<big>**Do**cker-based f**r**amework f**o**r ga**th**ering n**e**tflow tr**a**ffic</big>

## Description
The primary objective of this framework is to establish an environment that comprehensively monitors and captures all network flows on a `Docker` virtual network. All interactions within this virtual network are captured, parsed into flows, and subsequently exported to a CSV file.

### Old releases
The **DOROTHEA** project went throught a complete restructuring to simplify its architecture and enhance user-friendliness 🚧. We have drop all the Python scripts for handeling `DOROTHEA` in favour of a more minimalistic implementation using `Docker-Compose`.

If you are searching for one of the old implementations, we have tagged them as releases.

### Key Objectives

- **Realistic Netflow Generation:** The framework's primary objective is to generate flow that closely resemble real network traffic. These is archived by using real world tools to simulate genuine interactions and transactions, creating a robust dataset for training machine learning models.

- **Low Resource Consumption:** By establishing a virtual LAN and deploying containers as nodes, the framework creates a controlled, small-footprint environment that mimics real-world networking scenarios. This environment facilitates the generation and monitoring of traffic patterns while maintaining a low profile in resource consumption.

- **Effective & Flexible Monitoring:** The framework utilizes [`pmacct`](http://www.pmacct.net/) (Packet Monitoring Accounting) a tool for capturing and process network traffic. Utilizing the default `print` plugin, it allows us to capture and extract valuable insights from flows into a CSV without the need for a netflow collector, simplifying the process.


## Requirements

This tool requires to have installed in your system:
 - [Docker](https://www.docker.com/)
 - [Docker-Compose](https://docs.docker.com/compose/)

## Usage

Clone the repository with the following comand to ensure all the submodules are recursively fetch:
```bash
$ git clone --recursive https://github.com/uleroboticsgroup/DOROTHEA.git
$ cd DOROTHEA
```

On the `docker-compose.yml` file, add your containers that will generate any traffic after the comment:
```Python
# YOUR ACTIONS: ...
```

And finally simply run Docker-Compose:
```bash
$ docker compose .
```

## Examples

The examples directory includes various scenarios to emulate and capture network traffic of popular tools and interactions:

* [Port scan with nmap](examples/port-scan/README.md)
* [SSH brute force with HYDRA](examples/ssh-brute-force/README.md)


## License
This framework is released under the [LGPL-3.0](LICENSE). Feel free to use, modify, and distribute it in accordance with the terms of the license.

