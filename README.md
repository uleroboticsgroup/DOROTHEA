# DOROTHEA

[![Docker Image CI](https://github.com/uleroboticsgroup/DOROTHEA/actions/workflows/docker-image.yml/badge.svg)](https://github.com/uleroboticsgroup/DOROTHEA/actions/workflows/docker-image.yml)

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
 - Docker
 - Docker-Compose

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

## License
This framework is released under the [LGPL-3.0](LICENSE). Feel free to use, modify, and distribute it in accordance with the terms of the license.

